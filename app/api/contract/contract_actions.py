from sqlalchemy import text
from ..models.users import MintSign
from ..services import celery_scheduler
from . import (contract_address, contract_instance, private_key,
               public_address, web3)
from .helpers import create_nft, format_sign, make_gateway_url

import pdb

# pdb.set_trace()


def transfer_token(token_ids, to_address, from_address):
    transaction_hashes = []
    error_messages = {}

    for id_ in token_ids:
        token_owner = contract_instance.functions.ownerOf(id_).call()
        if token_owner == to_address:
            error_messages.update({id_: "Same TO & From address"})
        elif from_address != token_owner:
            error_messages.update({id_: "Token not owned by the 'from' address"})
        else:
            try:
                nonce = web3.eth.getTransactionCount(public_address, "latest")

                tx = contract_instance.functions.safeTransferFrom(from_address, to_address, id_).buildTransaction({
                    'chainId': web3.eth.chainId,
                    'gas': 2000000,
                    'gasPrice': web3.eth.gasPrice,
                    # 'gasPrice': web3.toWei('1', 'gwei'),
                    'nonce': nonce,
                })
                signed_tx = web3.eth.account.signTransaction(tx, private_key)
                resp = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                pdb.set_trace()

            except Exception as e:
                error_messages.update({id_: e})
    pdb.set_trace()

    return transaction_hashes, error_messages


# transfer_token([2], "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
#                "0x099446CAd9294C5537D8e2996f0d440C0cb381B3")


def withdraw_to_wallet():
    status = False

    try:
        nonce = web3.eth.getTransactionCount(public_address, "latest")

        tx = contract_instance.functions.withdraw().buildTransaction({
            'chainId': web3.eth.chainId,
            'gas': 2000000,
            'gasPrice': web3.eth.gasPrice,
            # 'gasPrice': web3.toWei('1', 'gwei'),
            'nonce': nonce,
            'from': public_address
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        status = True

    except Exception as e:
        print(e)

    return status


# withdraw_to_wallet()


def get_wallet_account_balance():
    balance = contract_instance.functions.balance().call({"from": public_address})
    return web3.fromWei(balance, "ether").to_eng_string()


def verify_transaction(hash):
    valid = False
    try:
        status = web3.eth.getTransactionReceipt(hash)['status']
        if int(status) == 1:
            valid = True
    except Exception as e:
        print(e)

    return valid


def get_token_uri(token_id) -> list:
    token = contract_instance.functions.tokenURI(token_id).call()
    if token:
        token = make_gateway_url(token)
    return token


def get_token_ids(account) -> list:
    balance = contract_instance.functions.balanceOf(account).call()
    token_ids = []
    for i in range(balance):
        id = contract_instance.functions.tokenOfOwnerByIndex(account, i).call()
        token_ids.append(id)
    return token_ids


def get_account_tokens(account) -> dict:
    token_ids = get_token_ids(account)
    tokens = {}
    for id_ in token_ids:
        token = get_token_uri(id_)
        tokens.update({id_: token})
    return tokens


def mint_token(user_address, tokenURI):

    nonce = web3.eth.getTransactionCount(contract_address, "latest")

    tx = {
        'nonce': nonce,
        'to': contract_address,
        'from': web3.eth.account.from_key(private_key).address,
        'chainId': web3.eth.chainId,
        'gas': 2000000,
        'gasPrice': web3.eth.gasPrice,
        'data': contract_instance.encodeABI(fn_name="mintToken",
                                            args=[user_address, tokenURI])
    }
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    try:
        tx_hash = web3.eth.sendRawTransaction(web3.toHex(signed_tx.rawTransaction))
        return tx_hash
    except Exception as e:
        print(e)


@celery_scheduler.task(name='complete-pending-transactions')
def complete_pending_transactions():
    mint_signs = MintSign.query.filter_by(
        minted=False).order_by(text("created_at")).all()

    for pending in mint_signs:
        if verify_transaction(pending.transaction_hash):
            sign = format_sign({"year": pending.dob.year,
                                "month": pending.dob.month,
                                "day": pending.dob.weekday(), })

            cid = create_nft(sign)
            if cid:
                tx_hash = mint_token(pending.user_address, cid)
                if tx_hash:
                    update_ = {
                        "mint_hash": tx_hash.hex(),
                        "minted": True,
                    }
                    print(update_)
                    pending.update(**update_)

            sign['user_address'] = pending.user_address
