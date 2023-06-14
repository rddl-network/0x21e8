import base58
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation, Transaction
from x21e8.models.transfer import Transfer

from x21e8.config import PLNTMNT_ENDPOINT
from x21e8.wallet.base_wallet import BaseWallet

import json
import ast


def create_cid_based_asset(cid: str, wallet: BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    pubkey = wallet.get_planetmint_pubkey()
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


def transfer(transfer_request: Transfer, wallet: BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)

    transferable_token = plntmnt.transactions.retrieve(transfer_request.token_id)
    transferable_tx = Transaction.from_dict(transferable_token)
    inputs = transferable_tx.to_inputs()

    amount = int(transfer_request.amount)
    input_amount = transferable_tx.outputs[transfer_request.output_id].amount
    if input_amount != amount:
        recipients = [
            ([transfer_request.recipient], amount),
            (transferable_tx.outputs[transfer_request.output_id].public_keys, input_amount - amount),
        ]
    else:
        recipients = [(transfer_request.recipient, amount)]

    transfer_tx = plntmnt.transactions.prepare(
        operation="TRANSFER",
        assets=[
            transferable_tx.id,
        ],
        inputs=[inputs[transfer_request.output_id].to_dict()],  # transfer_input,
        recipients=recipients,
    )
    signed_transfer_tx = fulfill_with_signing_delegation(transfer_tx, wallet.planetmint_sign_digest)
    ast_ = ast.literal_eval(str(signed_transfer_tx))
    json_obj_str = json.dumps(ast_)
    json_obj = json.loads(json_obj_str)
    transfer_transaction = plntmnt.transactions.send_commit(json_obj)
    return 200, transfer_transaction
