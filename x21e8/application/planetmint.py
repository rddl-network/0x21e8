import base58
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation
from x21e8.models.transfer import Transfer

from x21e8.config import PLNTMNT_ENDPOINT
from x21e8.wallet.base_wallet import BaseWallet

import json
import ast

def create_cid_based_asset(cid: str, wallet: BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    pubkey = wallet.get_planetmint_pubkey()
    print(pubkey)
    tx = plntmnt.transactions.prepare(
        operation="CREATE",
        signers=[base58.b58encode(pubkey).decode()],
        assets=[{"data": cid}],
    )

    signed_tx = fulfill_with_signing_delegation(tx, wallet.planetmint_sign_digest)
    token_nft = plntmnt.transactions.send_commit(signed_tx)
    return token_nft


def resolve_asset_token(asset: str):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    asset_tx = plntmnt.transactions.retrieve(asset)
    try:
        cid = asset_tx["asset"]["data"]
    except KeyError:
        raise KeyError  # TODO to be handled in a better way stating: this is not an rddl-asset
    return asset_tx, cid


def transfer_planetmint( transfer_request: Transfer, wallet: BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    
    transferable_token = plntmnt.transactions.retrieve( transfer_request.token_id)
    transferable_token_output = transferable_token["outputs"][transfer_request.output_id]
    transfer_input = {
        "fulfillment": transferable_token_output["condition"]["details"],
        "fulfills": {
            "output_index": 0,
            "transaction_id": transferable_token["id"],
        },
        "owners_before": transferable_token_output["public_keys"],
    }
    transfer_tx = plntmnt.transactions.prepare(
        operation="TRANSFER",
        assets=[transferable_token["id"],],
        inputs=transfer_input,
        recipients=transfer_request.recipient,
    )
    signed_transfer_tx = fulfill_with_signing_delegation(transfer_tx, wallet.planetmint_sign_digest)
    ast_ = ast.literal_eval(str(signed_transfer_tx))
    json_obj_str = json.dumps( ast_ )
    json_obj = json.loads( json_obj_str)
    transfer_transaction = plntmnt.transactions.send_commit(json_obj)
    return transfer_transaction
