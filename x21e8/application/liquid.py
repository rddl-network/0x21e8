import hashlib
import json
import six
import requests

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from x21e8.models.issuing_request import IssuingRequest
from x21e8.config import (
    LQD_RPC_ENDPOINT_SCHEMA,
    LQD_RPC_USER,
    LQD_RPC_PASSWORD,
    LQD_RPC_HOST,
    LQD_RPC_PORT,
    LIQUID_REGISTRATION_DOMAIN,
)
from x21e8.models.transfer import Transfer


TOKEN_AMOUNT = 1
VERSION = 0
FEE_RATE = 0.00001


class LiquidNode:
    def __init__(self):
        test = ""

    def _get_keys(self, rpc_connection: AuthServiceProxy):
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

        print(f"PubKey: {pubkey}")
        print(f"Asset_addr(_get_keys): {asset_addr}")
        print(f"token_addr(_get_keys): {token_addr}")

        return pubkey, asset_addr, token_addr

    def _create_contract(self, issue_request: IssuingRequest, nft_token: str, cid: str, pubkey: str):
        contract = f'{{"entity":{{"domain":"{LIQUID_REGISTRATION_DOMAIN}"}}, "issuer_pubkey":"{pubkey}", "nft":{{"token":"{nft_token}", "ipld":"{cid}"}}, "name":"{issue_request.name}", "precision":{issue_request.precision}, "ticker":"{issue_request.ticker}", "version":{VERSION}}}'
        contract = json.loads(contract)
        contract_sorted = json.dumps(contract, sort_keys=True, separators=(",", ":"))
        contract_hash = hashlib.sha256(six.ensure_binary(contract_sorted)).hexdigest()
        contract_hash_rev = "".join(reversed([contract_hash[i : i + 2] for i in range(0, len(contract_hash), 2)]))
        return contract, contract_hash_rev

    def issue_tokens(self, issue_request: IssuingRequest, nft_token: str, cid: str):
        rpc_connection = AuthServiceProxy(
            LiquidNode._get_liquid_auth_proxy_url(),
        )
        # TODO: comes in the next release: rpc_connection.loadwallet()
        # TODO: asset_addre could be removed
        # TODO: token_addr could be removed
        (pubkey, asset_addr, token_addr) = self._get_keys(rpc_connection=rpc_connection)

        (contract, contract_hash_rev) = self._create_contract(issue_request, nft_token, cid, pubkey)

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
        print(f"RIA: {ria}")

        brt = rpc_connection.blindrawtransaction(ria[0]["hex"], True, [], False)
        srt = rpc_connection.signrawtransactionwithwallet(brt)
        hex_srt = srt["hex"]

        issue_tx = rpc_connection.sendrawtransaction(hex_srt)
        asset = ria[0]["asset"]

        print("\n\n")
        print(f"ASSET: {asset}")
        print(f"TOKEN_ADDR: {token_addr}")
        print(f"ASSET_ADDR: {asset_addr}")
        print(f"ASSET_ID: {issue_tx}")
        print(f"CONTRACT: {contract}")
        return asset, issue_tx, contract

    def inject_key_into_liquid(self, wif_key: str):
        try:
            rpc_connection = AuthServiceProxy(
                LiquidNode._get_liquid_auth_proxy_url(),
            )
            IMPORTPRIVKEY = rpc_connection.importprivkey(wif_key, "tokenissuer", False)
            print(IMPORTPRIVKEY)
        except JSONRPCException as json_exception:
            print("A JSON RPX exception occured: " + str(json_exception))
        except Exception as general_exception:
            print("An exception occured: " + str(general_exception))

    @staticmethod
    def _get_liquid_auth_proxy_url():
        return f"{LQD_RPC_ENDPOINT_SCHEMA}://{LQD_RPC_USER}:{LQD_RPC_PASSWORD}@{LQD_RPC_HOST}:{LQD_RPC_PORT}"

    @staticmethod
    def register_asset(asset_id: str, contract: dict, registration_endpoint: str):
        json_obj = {"asset_id": asset_id, "contract": contract}
        response = requests.post(
            registration_endpoint,
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json=json_obj,
        )
        return response

    def transfer(self, transfer_request: Transfer):
        rpc_connection = AuthServiceProxy(
            LiquidNode._get_liquid_auth_proxy_url(),
        )
        # transfer an asset if token_id is defined or LBTC otherwise
        # doc @ https://elementsproject.org/en/doc/22.0.0/rpc/wallet/sendtoaddress/
        tx = rpc_connection.sendtoaddress(
            transfer_request.recipient,  # recipient address
            transfer_request.amount,  # amount
            "",  # comment
            "",  # comment-to
            False,  # subtractfeefromamount
            False,  # replaceable: True on mainnet, False on Testnet # TODO
            1,  # conf_target: Confirmation target in blocks
            "UNSET",  # estimate_mode
            False,  # avoid_reuse
            transfer_request.token_id,  # assetlabel: Hex asset id or asset label for balance.
        )
        print(f"tx info: {tx}")
        return 200, tx
