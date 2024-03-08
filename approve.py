from web3 import Web3, Account
import json




rpc_eth = 'https://eth-pokt.nodies.app'
w3 = Web3(Web3.HTTPProvider(rpc_eth))
# https://t.me/mallinmakin
# https://t.me/mallinmakin
# https://t.me/mallinmakin
ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"address","name":"admin_","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"stateMutability":"payable","type":"receive"}]''')

eth_contract_address = Web3.to_checksum_address('0x6774Bcbd5ceCeF1336b5300fb5186a12DDD8b367')
eth_contract = w3.eth.contract(eth_contract_address, abi=ERC20_ABI)


def bridge(account):
    address = account.address
    nonce = w3.eth.get_transaction_count(address)
    transaction = eth_contract.functions.swap(address, 20000000000000000, '', 168000).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 220000,
        'gasPrice': w3.eth.gas_price,
        'from': address,
        'nonce': nonce,
        'value': 20000000000000000

    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account.key)
    txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn


txt = 'privates.txt'
with open(txt, 'r', encoding='utf-8') as keys_file:
    accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
    for account in accounts:
        txn = bridge(account)
        print(f'https://etherscan.io///tx/{txn.hex()}')
