import base58
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation

from x21e8.config import PLNTMNT_ENDPOINT
from x21e8.wallet.base_wallet import BaseWallet



def create_cid_based_asset(cid: str, wallet: BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    pubkey = wallet.get_planetmint_pubkey()
    print(pubkey)
    tx = plntmnt.transactions.prepare(
        operation="CREATE",
        signers=[base58.b58encode(pubkey).decode()],
        asset={"data": cid},
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
