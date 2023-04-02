#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

#Algorand account credentials
#secret_key= "kxBGYHyTAXbXMB+FGVGMjrI4TtAPmOECPs127n2WuZ5IA5irH96bS/ge4luVcTDTKoMxQj7/Wpx7AbrzdjQWNA=="
account_address="JABZRKY732NUX6A64JNZK4JQ2MVIGMKCH37VVHD3AG5PG5RUCY2JWZOGAE"
mymnemonic_sk="bar blue coral daughter add talk mammal busy cost dutch economy cigar imitate bean leader object found way grief trash wink grain volume above ill"

def generate_account ():
    secret_key, address = account.generate_account()
    print(secret_key)
    print(address)
    mymnemonic_sk=mnemonic.from_private_key(secret_key)
    print(mymnemonic_sk)
    sk=mnemonic.to_private_key(mymnemonic_sk)
    print("Mnemonic works? ",sk==secret_key)
    return mymnemonic_sk, address

def send_tokens( receiver_pk, tx_amount ):
    sender_pk=account_address
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    params = acl.suggested_params()
    secret_key = mnemonic.to_private_key(mymnemonic_sk)
    unsigned_txn = transaction.PaymentTxn(
        sender=sender_pk,
        #gen_hash=params.gh,
        #first_valid_round = params.first,
        #tx_fee = params.min_fee,
        #last_valid_round = params.last,
        #receiver=receiver_pk,
        amt=tx_amount,
        note=b"Send tokens to test account",
    )

    signed_txn = unsigned_txn.sign(secret_key)

    txid = acl.send_transaction(signed_txn)
    txn_result = transaction.wait_for_confirmation(acl, txid)
    print("Transaction ID is: ", txid)
    print("Transaction result is: ", txn_result)

    return sender_pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
