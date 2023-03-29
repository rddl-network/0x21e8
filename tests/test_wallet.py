import pytest
from x21e8.wallet.sw_wallet import SoftwareWallet
from x21e8.application.token import token_transfer
from x21e8.models.transfer import Transfer


def test_libwally_key_creation():
    sw = SoftwareWallet()
    priv_wif_key = sw.derive_liquid_private_wif(0)
    assert len(priv_wif_key) == 52


@pytest.mark.parametrize(
    "symbol,id,token_id,recipient,exp_status,exp_message",
    [
        (
            "",
            8680,
            "5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
            "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
            404,
            "Not found",
        ),
        (
            "",
            0,
            "5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
            "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
            405,
            "Network ID or Symbol need to be defined",
        ),
        (
            "",
            10,
            "5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
            "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
            405,
            "Network ID or Symbol have to be supported",
        ),
        (
            "SDF",
            0,
            "5a7037f4899f16c6e41ba20a2473be3e5f1e7df5f922df3e3a37e3c214894e51",
            "6B3NgjZbL2mQTZNzitq1zoCZjgKrRA16KfPAbhWXYAaz",
            405,
            "Network ID or Symbol have to be supported",
        ),
        (
            "LBTC",
            0,
            "34bf2432dfd308d08ab5acc30e1a4d4c79ffdce822ac22b6a8fcaae082c0ead4",
            "tex1qw26uvnvp3zmw6zk3k0p23xkt4k96zchkl409mh",
            426,
            "Insufficient funds",
        ),
        (
            "",
            998,
            "34bf2432dfd308d08ab5acc30e1a4d4c79ffdce822ac22b6a8fcaae082c0ead3",
            "tex1qw26uvnvp3zmw6zk3k0p23xkt4k96zchkl409mh",
            200,
            "",
        ),
    ],
)
def test_token_transfer(symbol, id, token_id, recipient, exp_status, exp_message):
    t_object = Transfer(
        network_slip_symbol=symbol,
        network_slip_id=id,
        account=0,
        change=0,
        index=0,
        token_id=token_id,
        output_id=0,
        amount=1.0,
        recipient=recipient,
        is_confidential=False,
    )
    response = token_transfer(t_object)
    assert response[0] == exp_status
    if symbol == "LBTC" or id == 998:
        if response[0] < 400:  # a positive request
            assert len(response[1]) == 64
        else:
            assert response[1] == exp_message
    else:
        assert response[1] == exp_message
