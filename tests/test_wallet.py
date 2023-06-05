import pytest
from x21e8 import wallet
from x21e8.application.planetmint import create_cid_based_asset
from x21e8.wallet.sw_wallet import SoftwareWallet
from x21e8.application.token import token_transfer
from x21e8.models.transfer import Transfer
from x21e8.utils.storage import store_asset
from planetmint_cryptoconditions.crypto import Ed25519SigningKey, Ed25519VerifyingKey


def test_libwally_key_creation():
    sw = SoftwareWallet()
    priv_wif_key = sw.derive_liquid_private_wif(0)
    assert len(priv_wif_key) == 52


@pytest.mark.liquid
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
def test_token_transfer_divisible(symbol, id, token_id, recipient, exp_status, exp_message):
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


def test_fungible_token_transfer_planetmint():
    from planetmint_driver import Planetmint
    from planetmint_driver.offchain import fulfill_with_signing_delegation
    from x21e8.config import PLNTMNT_ENDPOINT
    import base58
    import datetime

    cid = store_asset(str({"test": "test" + str(datetime.datetime.now())}))
    wallet = SoftwareWallet()
    plntmnt = Planetmint(PLNTMNT_ENDPOINT)
    pubkey_raw = wallet.get_planetmint_pubkey()
    pubkey = base58.b58encode(pubkey_raw).decode()
    print(pubkey)
    tx = plntmnt.transactions.prepare(
        operation="CREATE", signers=[pubkey], assets=[{"data": cid}], recipients=[([pubkey], 100)]
    )

    signed_tx = fulfill_with_signing_delegation(tx, wallet.planetmint_sign_digest)
    token_nft = signed_tx
    try:
        token_nft = plntmnt.transactions.send_commit(signed_tx)
    except Exception as e:
        print(f"EXCEPTION {e}")

    t_object = Transfer(
        network_slip_symbol="PLMNT",
        network_slip_id=8680,
        account=0,
        change=0,
        index=0,
        token_id=token_nft["id"],
        output_id=0,
        amount=30.0,
        recipient=pubkey,
        is_confidential=False,
    )
    status, message = token_transfer(t_object)
    assert status == 200
    assert isinstance(message, dict)
    assert "assets" in message
    assert "id" in message
    assert "outputs" in message
    assert len(message["outputs"]) == 2
    assert message["outputs"][0]["amount"] == "30"
    assert message["outputs"][1]["amount"] == "70"


def test_get_address():
    wallet = SoftwareWallet()
    liquid_address = wallet.get_liquid_address()
    planemint_address = wallet.get_planetmint_address()

    result = {"liquid address": liquid_address, "planetmint address": planemint_address}
    assert len(liquid_address) == 34
    assert len(planemint_address) == 44
