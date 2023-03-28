from x21e8.wallet.sw_wallet import SoftwareWallet
from x21e8.application.token import token_transfer
from x21e8.models.transfer import Transfer

def test_libwally_key_creation():
    sw = SoftwareWallet()
    priv_wif_key = sw.derive_liquid_private_wif(0)
    assert len(priv_wif_key) == 52

def test_token_transfer():
    t_object = Transfer( 
            network_slip_symbol="",
            network_slip_id = 8680,
            account=0,
            change=0,
            index=0,
            token_id = "5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
            output_id=0,
            amount = 1.0,
            recipient= "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
            is_confidential=False,            
            )
    response = token_transfer( t_object )
