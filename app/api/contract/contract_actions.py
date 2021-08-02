from app.api.helpers.signs import check_existing_user
from hashlib import md5

from app import celery_app
from celery.utils.log import get_task_logger
from sqlalchemy import text

from ...services.memecache import memcache_lock
from ..models.users import MintSign
from . import (contract_address, contract_instance, private_key,
               public_address, web3)
from .helpers import (create_nft, format_sign,
                      get_nft_data, make_gateway_url,
                      strip_ipfs_uri_prefix)

from ..models import NFT

logger = get_task_logger(__name__)


def value_based_gas_price_strategy(web3, transaction_params):
    if transaction_params['value'] > web3.toWei(1, 'ether'):
        return web3.toWei(20, 'gwei')
    else:
        return web3.toWei(5, 'gwei')


def withdraw_to_wallet():
    nonce = web3.eth.getTransactionCount(public_address, "latest")
    # web3.eth.setGasPriceStrategy(value_based_gas_price_strategy)

    tx = {
        'nonce': web3.toHex(nonce),
        'to': contract_address,
        'from': web3.eth.account.from_key(private_key).address,
        'chainId': web3.eth.chainId,
        'gasPrice': web3.toHex(web3.eth.gasPrice),
        'data': contract_instance.encodeABI(fn_name="withdraw", args=[])
    }
    tx['gas'] = web3.toHex(web3.eth.estimateGas(tx))

    signed_tx = web3.eth.account.signTransaction(tx, private_key)

    try:
        tx_hash = web3.eth.sendRawTransaction(web3.toHex(signed_tx.rawTransaction))
        # import pdb
        # pdb.set_trace()
        return tx_hash
    except Exception as e:
        print(e)
        # import pdb
        # pdb.set_trace()


# txn = contract_instance.functions.withdraw().buildTransaction(data)
# signed_txn = web3.eth.account.signTransaction(txn, private_key)
# tx_hash = web3.toHex(web3.eth.sendRawTransaction(signed_txn.rawTransaction))
# contract_instance.functions.setWallet(web3.eth.account.from_key(private_key).address).transact(data)
# # tx['gas'] = web3.eth.estimateGas(tx)
# signed_tx = web3.eth.account.signTransaction(tx, private_key)
# resp = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


def get_wallet_account_balance():
    balance = contract_instance.functions.balance().call({"from": public_address})
    return web3.toWei(balance, "ether")


def verify_transaction(hash):
    valid = False
    try:
        status = web3.eth.getTransactionReceipt(hash)['status']
        if int(status) == 1:
            valid = True
    except Exception as e:
        print(e)

    return valid


def get_total_supply() -> int:
    tokens = contract_instance.functions.totalSupply().call()
    return tokens


def get_token_uri(token_id, get_uri=True) -> str:
    token = contract_instance.functions.tokenURI(token_id).call()
    if token and get_uri:
        token = make_gateway_url(token)
    return token


@celery_app.task(name='list-minted-tokens')
def format_tokens():
    total_supply = get_total_supply()
    for i in range(1, total_supply + 1):
        nft = NFT.query.filter_by(token_id=i).first()
        if not nft:
            token_uri = strip_ipfs_uri_prefix(get_token_uri(i, False))
            nft_metadata = get_nft_data(token_uri)
            if nft_metadata:
                urls = make_gateway_url(token_uri, nft_metadata)
                nft = NFT({"token_id": i,
                           "token_url": get_token_uri(i, False),
                           "gateway_token_url": make_gateway_url(token_uri),
                           "image_url": urls['image_url'],
                           "token_metadata": urls['token_metadata'],
                           "metadata_url": urls['metadata_url']})
                nft.save()

        elif nft and not nft.token_url:
            token_uri = get_token_uri(i, False)
            nft.update(**{"gateway_token_url": make_gateway_url(token_uri),
                          "token_url": token_uri})


@celery_app.task(name='assign-nfts-to-user', bind=True)
def assign_nfts_to_users(self):
    total_supply = get_total_supply()
    for i in range(1, total_supply + 1):
        nft = NFT.query.filter_by(token_id=i).first()
        if nft:
            nft_hexdigest = md5(str(i).encode()).hexdigest()
            lock_id = '{0}-lock-{1}'.format(self.name, nft_hexdigest)
            logger.debug('Handling Transaction: %s', nft)
            with memcache_lock(lock_id, self.app.oid) as acquired:
                if acquired:
                    token_owner = contract_instance.functions.ownerOf(i).call()
                    user = check_existing_user({"address": token_owner})
                    user.add_nft(nft)

            logger.debug(
                'NFT %s is already being handled by another worker', i)


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
        'gasPrice': web3.toHex(web3.eth.gasPrice),
        'data': contract_instance.encodeABI(fn_name="mintToken",
                                            args=[user_address,
                                                  tokenURI])
    }
    tx['gas'] = web3.toHex(web3.eth.estimateGas(tx))
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
            'Transaction %s is already being handled by another worker', transaction_hash)


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
