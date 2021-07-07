from hashlib import md5

from app import celery_app
from celery.utils.log import get_task_logger
from sqlalchemy import text

from ...services.memecache import memcache_lock
from ..models.users import MintSign
from . import (contract_address, contract_instance, private_key,
               public_address, web3)
from .helpers import create_nft, format_sign, make_gateway_url

logger = get_task_logger(__name__)


# def transfer_token(token_ids, to_address, from_address):
#     transaction_hashes = []
#     error_messages = {}

#     for id_ in token_ids:
#         token_owner = contract_instance.functions.ownerOf(id_).call()
#         if token_owner == to_address:
#             error_messages.update({id_: "Same TO & From address"})
#         elif from_address != token_owner:
#             error_messages.update({id_: "Token not owned by the 'from' address"})
#         else:
#             try:
#                 nonce = web3.eth.getTransactionCount(public_address, "latest")

#                 tx = contract_instance.functions.safeTransferFrom(
#                     from_address, to_address, id_).buildTransaction({
#                         'chainId': web3.eth.chainId,
#                         'gas': 2000000,
#                         'gasPrice': web3.eth.gasPrice,
#                         # 'gasPrice': web3.toWei('1', 'gwei'),
#                         'nonce': nonce,
#                         'from': from_address
#                     })
#                 import pdb
#                 pdb.set_trace()
#                 signed_tx = web3.eth.account.signTransaction(tx, private_key)
#                 import pdb
#                 pdb.set_trace()
#                 resp = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

#             except Exception as e:
#                 error_messages.update({id_: e})

#     return transaction_hashes, error_messages


# transfer_token([32], "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
#                "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")


def withdraw_to_wallet():
    tx_hash = ""

    try:
        nonce = web3.eth.getTransactionCount(public_address, "latest")

        data = {
            'nonce': nonce,
            'from': web3.eth.account.from_key(private_key).address,
            'chainId': web3.eth.chainId
        }

        txn = contract_instance.functions.withdraw().buildTransaction(data)
        signed_txn = web3.eth.account.signTransaction(txn, private_key)
        tx_hash = web3.toHex(web3.eth.sendRawTransaction(signed_txn.rawTransaction))
        # import pdb
        # pdb.set_trace()
        # contract_instance.functions.withdraw().transact()
        # # tx['gas'] = web3.eth.estimateGas(tx)
        # signed_tx = web3.eth.account.signTransaction(tx, private_key)
        # resp = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    except Exception as e:
        print(e)

    return tx_hash


# print(withdraw_to_wallet())


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

    nonce = web3.eth.getTransactionCount(public_address, "latest")

    tx = {
        'nonce': nonce,
        'to': contract_address,
        'from': web3.eth.account.from_key(private_key).address,
        'chainId': web3.eth.chainId,
        # 'gas': web3.toHex(2000000),
        'gasPrice': web3.toHex(web3.eth.gasPrice),
        'data': contract_instance.encodeABI(fn_name="mintToken",
                                            args=[user_address, tokenURI])
    }
    tx['gas'] = web3.eth.estimateGas(tx)
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    try:
        tx_hash = web3.eth.sendRawTransaction(web3.toHex(signed_tx.rawTransaction))
        return tx_hash
    except Exception as e:
        print(e)


@celery_app.task(name='complete-pending-transactions', bind=True)
def complete_pending_transactions(self):
    mint_signs = MintSign.query.filter_by(
        minted=False).order_by(text("created_at")).all()

    for pending in mint_signs:
        transaction_hash = pending.transaction_hash
        # The cache key consists of the task name and the MD5 digest
        # of the feed URL.
        transaction_hash_hexdigest = md5(transaction_hash.encode()).hexdigest()
        lock_id = '{0}-lock-{1}'.format(self.name, transaction_hash_hexdigest)
        logger.debug('Handling Transaction: %s', transaction_hash)
        with memcache_lock(lock_id, self.app.oid) as acquired:
            if acquired:
                if verify_transaction(transaction_hash):
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

        logger.debug(
            'Feed %s is already being imported by another worker', transaction_hash)
