import pdb

from app import celery_app
from sqlalchemy import text

from ..models.users import MintSign
from ..services import celery_scheduler
from . import (contract_address, contract_instance, private_key,
               public_address, web3)
from .helpers import create_nft, format_sign, make_gateway_url

# def pay_minting_fee(account):
#     nonce = web3.eth.getTransactionCount(contract_address, 'latest')
#     amountToSend = 400000000000000
#     weiAmount = web3.toWei(amountToSend, 'wei')

#     tx = {
#         "from": account,
#         "nonce": web3.toHex(nonce),
#         "value": weiAmount,
#     }
#     gasEstimate = web3.eth.estimateGas(tx)

#     tx['gasPrice'] = web3.toHex(int(web3.toWei(str(gasEstimate), 'gwei') / 100))
#     tx['gasLimit'] = web3.toHex(gasEstimate * 2)
#     import pdb; pdb.set_trace()

#     errorMessage = None
#     transactionHash = None

# pay_minting_fee(test_address)
# import pdb; pdb.set_trace()


def verify_transaction(hash):
    valid = False
    try:
        status = web3.eth.getTransactionReceipt(hash)['status']
        if int(status) == 1:
            valid = True
    except Exception as e:
        print(e)

    return valid


# pdb.set_trace()


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


@celery_app.task(name='get-tokens')
def get_account_tokens(account) -> dict:
    token_ids = get_token_ids(account)
    tokens = {}
    for id_ in token_ids:
        token = get_token_uri(id_)
        tokens.update({id_: token})
    return tokens


# user_tokens = get_account_tokens("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
# pdb.set_trace()


def mint_token(user_address, tokenURI):

    nonce = web3.eth.getTransactionCount(contract_address, "latest")

    nonce = web3.eth.getTransactionCount(public_address)

    tx = {
        'nonce': nonce,
        'to': contract_address,
        'from': web3.eth.account.from_key(private_key).address,
        'chainId': web3.eth.chainId,
        'gas': 2000000,
        'gasPrice': web3.eth.gasPrice,
        'data': contract_instance.encodeABI(fn_name="mintToken", args=[user_address, tokenURI])
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


# complete_pending_transactions()
# pdb.set_trace()
