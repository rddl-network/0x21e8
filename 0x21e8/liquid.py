from model import IssuingRequest
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import base64
import hashlib
import json
import time
import six
import sys
import os

# rpc_port = 18886
rpc_port = 8000
rpc_user = 'user1'
rpc_password = 'password1'
DOMAIN = "lab.r3c.network"

TOKEN_AMOUNT = 1
VERSION = 0
FEERATE = 0.03000000


def issue_tokens(issueTokens: IssuingRequest, issuer_address, nft_token, ipdl):
    NAME = issueTokens.name
    TICKER = issueTokens.ticker
    ASSET_AMOUNT = issueTokens.amount
    PRECISION = issueTokens.precision

    VALIDATEADDR = None
    PUBKEY = None
    ASSET_ADDR = None
    TOKEN_ADDR = None
    rpc_connection = None
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, DOMAIN, rpc_port))
        NEWADDR = rpc_connection.getnewaddress("riddlemint", "legacy")
        VALIDATEADDR = rpc_connection.getaddressinfo(NEWADDR)
        PUBKEY = VALIDATEADDR["pubkey"]
        ASSET_ADDR = NEWADDR
        NEWADDR = rpc_connection.getnewaddress("MoteMagic", "legacy")
        TOKEN_ADDR = NEWADDR

    except JSONRPCException as json_exception:
        print("A JSON RPX exception occured: " + str(json_exception))
    except Exception as general_exception:
        print("An exception occured: " + str(general_exception))

    print(VALIDATEADDR)
    print(PUBKEY)
    print(ASSET_ADDR)
    print(TOKEN_ADDR)

    CONTRACT = f"{{\"entity\":{{\"domain\":\"{DOMAIN}\"}}, \"issuer_pubkey\":\"{PUBKEY}\", \"nft\":{{\"token\":\"{nft_token}\", \"ipld\":\"{ipdl}\"}}, \"name\":\"{NAME}\", \"precision\":{PRECISION}, \"ticker\":\"{TICKER}\", \"version\":{VERSION}}}"
    rpc_connection.settxfee(FEERATE)
    print(CONTRACT)
    CONTRACT_SORTED = json.dumps(json.loads(CONTRACT), sort_keys=True, separators=(",", ":"))
    CONTRACT_HASH = hashlib.sha256(six.ensure_binary(CONTRACT_SORTED)).hexdigest()
    print(CONTRACT_HASH)
    CONTRACT_HASH_REV = "".join(reversed([CONTRACT_HASH[i:i + 2] for i in range(0, len(CONTRACT_HASH), 2)]))
    print(CONTRACT_HASH_REV)

    RAWTX = rpc_connection.createrawtransaction([], [{"data": "00"}])

    print(RAWTX)

    # get funded raw transaction
    FRT = rpc_connection.fundrawtransaction(RAWTX, {"feeRate": FEERATE})
    print(FRT)

    HEXFRT = FRT["hex"]
    print(HEXFRT)

    RIA = rpc_connection.rawissueasset(HEXFRT, [{"asset_amount": ASSET_AMOUNT,
                                                 "asset_address": ASSET_ADDR,
                                                 "token_amount": TOKEN_AMOUNT,
                                                 "token_address": TOKEN_ADDR,
                                                 "blind": False,
                                                 "contract_hash": CONTRACT_HASH_REV, }])
    print(RIA)

    HEXRIA = RIA[0]["hex"]
    ASSET = RIA[0]["asset"]
    ENTROPY = RIA[0]["entropy"]
    TOKEN = RIA[0]["token"]

    BRT = rpc_connection.blindrawtransaction(HEXRIA, True, [], False)
    SRT = rpc_connection.signrawtransactionwithwallet(BRT)
    HEXSRT = SRT["hex"]

    ##  TEST = rpc_connection.testmempoolaccept(['"' + HEXSRT + '"'])
    TEST = rpc_connection.testmempoolaccept([HEXSRT])
    ALLOWED = TEST[0]["allowed"]
    print(ALLOWED)

    ISSUETX = rpc_connection.sendrawtransaction(HEXSRT)

    print("\n\n")
    print(F"ASSET_ID: {ISSUETX}")
    print(F"CONTRACT: {CONTRACT}")
    return ISSUETX