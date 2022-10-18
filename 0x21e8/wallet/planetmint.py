from . import base_wallet
import base58
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation


def attest_planet_mint_nft( cid: str, wallet: base_wallet.BaseWallet):
    plntmnt = Planetmint('https://test.ipdb.io')
    pubkey = wallet.get_planetmint_pubkey()
    print(pubkey)
    tx = plntmnt.transactions.prepare(
        operation='CREATE',
        signers=[base58.b58encode(pubkey).decode()],
        asset={'data': { 'cid': cid } })

    signed_tx = fulfill_with_signing_delegation(tx, wallet.planetmint_sign_digest)
    token_nft = plntmnt.transactions.send_commit(signed_tx)
    return token_nft
