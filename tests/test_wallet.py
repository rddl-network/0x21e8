from x21e8.wallet.sw_wallet import SoftwareWallet


def test_libwally_key_creation():
    sw = SoftwareWallet()
    priv_wif_key = sw.derive_liquid_private_wif(0)
    assert len(priv_wif_key) == 52
