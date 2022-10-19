from . import base_wallet
import base58
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation

from config import PLNTMNT_ENDPOINT

def attest_cid(cid: str, wallet: base_wallet.BaseWallet):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    pubkey = wallet.get_planetmint_pubkey()
    print(pubkey)
    tx = plntmnt.transactions.prepare(
        operation="CREATE", signers=[base58.b58encode(pubkey).decode()], asset={"data": {"cid": cid}}
    )

    signed_tx = fulfill_with_signing_delegation(tx, wallet.planetmint_sign_digest)
    token_nft = plntmnt.transactions.send_commit(signed_tx)
    return token_nft


def get_nft(nft: str):
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    nft_tx = plntmnt.transactions.retrieve(nft)
    nft_tx["asset"]["data"]["cid"]
    try:
        cid = nft_tx["asset"]["data"]["cid"]
    except KeyError:
        raise KeyError  # TODO to be handled in a better way stating: this is not an rddl-asset
    return nft_tx, cid
