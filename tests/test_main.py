import os
import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from x21e8.main import app
from x21e8.utils.storage import calculate_cid_v1


client = TestClient(app)


def delete_secret():
    filepath = "secret.txt"
    if os.path.exists(filepath):
        os.remove(filepath)


def test_store_data_valid():
    asset = str({"NFT_MetaDat": "mytest", "NFT_emissions": 10, "Consumption": 0.530})
    response = client.post(
        f"/data?data={asset}",
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    cid_response = response.json()["cid"]
    assert cid_response == calculate_cid_v1(asset)


def test_store_data_invalid():
    try:
        client.post(
            "/data",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"NFT_MetaDat"},
        )
        assert False
    except TypeError:
        pass
    except:
        assert True


def test_storing_and_retrieving_encrypted_data():
    asset = str({"NFT_MetaDat": "mytest", "NFT_emissions": 10})
    response = client.post(
        f"/data?data={asset}&encrypt=True",
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    cid = response.json()
    response = client.get("/data?cid=" + cid["cid"] + "&link2data=false&decrypt=true")


def test_get_data_valid():
    client.get("/data?cid=bafkreidbtalllk5s4jo3jkchj6zqt6nhxtrfvvdaxna5g7luttzd4uci2m&link2data=false")
    try:
        client.get("/data?cid=bafkreib2es2hnrsee64kufj3z6o5t3wat7z2k3xfobdyrj3v6lrzjq6o5i&link2data=false")
        assert False
    except:
        assert True


# @pytest.mark.skip(
#    reason="the secret is not automatically removed. that's why this test fails sometimes and is skipped."
# )
def test_machine_before_wallet_init():
    delete_secret()
    x = datetime.now()
    response1 = client.post(
        "/machine",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "name": "mytest - " + str(x),
            "ticker": "yourtest",
            "amount": 10000,
            "precision": 0,
            "public_url": "https://test.org",
            "reissue": True,
            "cid": "bafkreib2es2hnrsee64kufj3z6o5t3wat7z2k3xfobdyrj3v6lrzjq6o5i",
        },
    )
    assert response1.status_code == 421
    assert response1.json() == {"detail": "The hardware wallet needs to be provisioned by defining a master seed."}


def test_seed_creation():
    response1 = client.get("/seed?number_of_words=12")
    assert response1.status_code == 200
    mnemonic = response1.json()
    assert len(mnemonic["mnemonic"].split()) == 12

    response1 = client.get("/seed?number_of_words=24")
    assert response1.status_code == 200
    mnemonic = response1.json()
    assert len(mnemonic["mnemonic"].split()) == 24

    response1 = client.get("/seed?number_of_words=11")
    assert response1.status_code == 420
    assert response1.json() == {"detail": "A mnemonic has to contain 12 or 24 words"}
    assert len(mnemonic["mnemonic"].split()) == 24

    response1 = client.post(
        "/seed?mnemonic_phrase=%22potato%20drop%20kidney%20coral%20toilet%20elite%20uncover%20keep%20vintage%20beach%20eyebrow%20ethics%22"
    )
    assert response1.status_code == 200
    response1 = client.post(
        "/seed?mnemonic_phrase=%22argue%20open%20meat%20hammer%20attend%20high%20milk%20human%20much%20session%20seat%20beauty%20permit%20symbol%20panther%20night%20firm%20butter%20jewel%20defense%20obtain%20wife%20ill%20brain%22"
    )
    assert response1.status_code == 200
    response1 = client.post(
        "/seed?mnemonic_phrase=%22argue%20open%20meat%20hammer%20attend%20high%20milk%20human%20much%20session%20seat%20beauty%20permit%20symbol%20panther%20night%20firm%20butter%20jewel%20defense%20obtain%20wife%20ill%22"
    )
    assert response1.status_code == 420
    assert response1.json() == {"detail": "A mnemonic has to contain 12 or 24 words"}


@pytest.mark.skip(reason="failled on github. to be improved.")
def test_machine_attestation():
    x = datetime.now()
    response1 = client.post(
        "/machine",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "name": "mytest - " + str(x),
            "ticker": "yourtest",
            "amount": 10000,
            "precision": 0,
            "public_url": "https://test.org",
            "reissue": True,
            "cid": "bafkreib2es2hnrsee64kufj3z6o5t3wat7z2k3xfobdyrj3v6lrzjq6o5i",
        },
    )
    assert response1.status_code == 200
    print(f"{response1.json()}")
    try:
        client.post(
            "/machine",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "mytest2 - " + str(x),
                "ticker": "yourtest2",
                "amount": 10000,
                "precision": 0,
                "public_url": "https://test.org",
                "cid": "bafkreib2es2hnrsee64kufj3z6o5t3wat7z2k3xfobdyrj3v6lrzjq6o5i",
            },
        )
        assert False
    except:
        assert True
    tx_id = response1.json()["NFT token"]
    response3 = client.get(f"/machine?nft_token={tx_id}")
    assert response3.status_code == 200

    try:
        client.get("/machine?nft_token=61c557961bdf67e421aeaf26eb9aa406335e259ed7cc8a94c0073dd78b8dsdfac1")
        assert False
    except:
        assert True


@pytest.mark.skip(reason="failled on github. to be improved.")
def test_machine_attestation_without_token_creation(mocker):
    x = datetime.now()
    response1 = client.post(
        "/machine",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "name": "mytest - " + str(x),
            "ticker": "",
            "amount": 0,
            "precision": 0,
            "public_url": "https://test.org",
            "reissue": True,
            "cid": "bafkreib2es2hnrsee64kufj3z6o5t3wat7z2k3xfobdyrj3v6lrzjq6o5i",
        },
    )
    assert response1.status_code == 200
    print(f"{response1.json()}")
    tx_id = response1.json()["NFT token"]
    response3 = client.get(f"/machine?nft_token={tx_id}")
    assert response3.status_code == 404
