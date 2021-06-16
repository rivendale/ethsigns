import json
import os
import pdb

from config import AppConfig

web3 = AppConfig.web3

contract_instance = None
public_address = None

contract_address = AppConfig.CONTRACT_ADDRESS
private_key = AppConfig.PRIVATE_KEY
ipfs_url = AppConfig.IPFS_GATEWAY_URL
test_address = "0x099446CAd9294C5537D8e2996f0d440C0cb381B3"

script_dir = os.path.dirname(__file__)
abi_path = os.path.join(script_dir, 'abi.json')

abi = {}

with open(abi_path) as contract_json:
    data = contract_json.read()
    abi = json.loads(data)['abi']
if web3:
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)

    public_address = web3.eth.account.from_key(private_key).address
