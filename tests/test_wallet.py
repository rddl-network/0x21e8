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
        network_slip_id=8680,
        account=0,
        change=0,
        index=0,
        token_id="5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
        output_id=0,
        amount=1.0,
        recipient="6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
        is_confidential=False,
    )
    response = token_transfer(t_object)


def test_token_transfer_no_network():
    t_object = Transfer(
        network_slip_symbol="",
        network_slip_id=0,
        account=0,
        change=0,
        index=0,
        token_id="5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
        output_id=0,
        amount=1.0,
        recipient="6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == 405
    assert response[1] == "Network ID or Symbol need to be defined"


def test_token_transfer_invalid_network():
    t_object = Transfer(
        network_slip_symbol="",
        network_slip_id=10,
        account=0,
        change=0,
        index=0,
        token_id="5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
        output_id=0,
        amount=1.0,
        recipient="6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == 405
    assert response[1] == "Network ID or Symbol have to be supported"


def test_token_transfer_invalid_network_symbol():
    t_object = Transfer(
        network_slip_symbol="SDF",
        network_slip_id=0,
        account=0,
        change=0,
        index=0,
        token_id="5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
        output_id=0,
        amount=1.0,
        recipient="6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == 405
    assert response[1] == "Network ID or Symbol have to be supported"


def test_token_transfer_invalid_network_symbol():
    t_object = Transfer(
        network_slip_symbol="SDF",
        network_slip_id=0,
        account=0,
        change=0,
        index=0,
        token_id="5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
        output_id=0,
        amount=1.0,
        recipient="6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == 405
    assert response[1] == "Network ID or Symbol have to be supported"

def test_token_transfer_valid_LBTC():
    t_object = Transfer(
        network_slip_symbol="LBTC",
        network_slip_id=0,
        account=0,
        change=0,
        index=0,
        token_id="34bf2432dfd308d08ab5acc30e1a4d4c79ffdce822ac22b6a8fcaae082c0ead3",
        output_id=0,
        amount=1.0,
        recipient="tex1qw26uvnvp3zmw6zk3k0p23xkt4k96zchkl409mh",
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == 200
