# This function takes a message as an argument, converts it to byte format, and sends it as part of an
# Ethereum transaction on the Goerli network. The transaction is signed using a specified private key, and the
# hexadecimal hash of the transaction is returned as the result.

from web3 import Web3


def send_transaction(message):
    w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/9e9789a285bd4fdb80c4d5dfc97cb246'))
    address = '0xE89E8908758CDc640b3feaDE40D7e50c62861359'
    privateKey = '0xbf89c20236f489492fafa80bbe55cc84df1f2fc9d23109073aeef0a589c53852'
    nonce = w3.eth.get_transaction_count(address)
    gasPrice = w3.eth.gas_price
    value = w3.to_wei(0, 'ether')
    signedTx = w3.eth.account.sign_transaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.send_raw_transaction(signedTx.rawTransaction)
    txId = w3.to_hex(tx)
    return txId