import hashlib
import json
import six
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from x21e8.model import IssuingRequest
from x21e8.config import build_liquid_auth_proxy_url

TOKEN_AMOUNT = 1
VERSION = 0
FEE_RATE = 0.03000000


def get_keys(rpc_connection: AuthServiceProxy):
    pubkey = None
    asset_addr = None
    token_addr = None
    try:
        new_addr = rpc_connection.getnewaddress("riddlemint", "legacy")  # args: label, address type
        validate_addr = rpc_connection.getaddressinfo(new_addr)
        pubkey = validate_addr["pubkey"]
        asset_addr = new_addr
        new_addr = rpc_connection.getnewaddress("MoteMagic", "legacy")  # args: label, address type
        token_addr = new_addr
    except JSONRPCException as json_exception:
        print("A JSON RPX exception occured: " + str(json_exception))
    except Exception as general_exception:
        print("An exception occured: " + str(general_exception))
    
    print(pubkey)
    print(asset_addr)
    print(token_addr)
    
    return (pubkey, asset_addr, token_addr)


def create_contract(issue_request: IssuingRequest, nft_token:str, cid:str, pubkey:str):
    
    contract = f'{{"entity":{{"domain":"{issue_request.public_url}"}}, "issuer_pubkey":"{pubkey}", "nft":{{"token":"{nft_token}", "ipld":"{cid}"}}, "name":"{issue_request.name}", "precision":{issue_request.precision}, "ticker":"{issue_request.ticker}", "version":{VERSION}}}'
    contract_sorted = json.dumps(json.loads(contract), sort_keys=True, separators=(",", ":"))
    contract_hash = hashlib.sha256(six.ensure_binary(contract_sorted)).hexdigest()
    contract_hash_rev = "".join(reversed([contract_hash[i : i + 2] for i in range(0, len(contract_hash), 2)]))
    print(contract)
    print(contract_hash)
    print(contract_hash_rev)
    return (contract, contract_hash_rev)


def issue_tokens(issue_request: IssuingRequest, nft_token:str, cid:str):

    rpc_connection = AuthServiceProxy(
        build_liquid_auth_proxy_url(),
    )

    (pubkey, asset_addr, token_addr) = get_keys(rpc_connection=rpc_connection)

    (contract, contract_hash_rev) = create_contract(issue_request, nft_token, cid, pubkey)

    rpc_connection.settxfee(FEE_RATE)
    raw_tx = rpc_connection.createrawtransaction([], [{"data": "00"}])
    print(raw_tx)

    # get funded raw transaction
    frt = rpc_connection.fundrawtransaction(raw_tx, {"feeRate": FEE_RATE})
    print(frt)
    hex_frt = frt["hex"]
    print(hex_frt)

    ria = rpc_connection.rawissueasset(
        hex_frt,
        [
            {
                "asset_amount": issue_request.amount,
                "asset_address": asset_addr,
                "token_amount": TOKEN_AMOUNT,
                "token_address": token_addr,
                "blind": False,
                "contract_hash": contract_hash_rev,
            }
        ],
    )
    print(ria)

    brt = rpc_connection.blindrawtransaction(ria[0]["hex"], True, [], False)
    srt = rpc_connection.signrawtransactionwithwallet(brt)
    hex_srt = srt["hex"]

    issue_tx = rpc_connection.sendrawtransaction(hex_srt)

    print("\n\n")
    print(f"ASSET_ID: {issue_tx}")
    print(f"CONTRACT: {contract}")
    return issue_tx, contract
