from fastapi.testclient import TestClient
import logging
import requests
import base58

LOGGER = logging.getLogger(__name__)
from main import app

# from main import w3s

client = TestClient(app)


def test_read_valid():
    try:
        response = client.post(
            "/store_data",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"NFT_MetaDat": "mytest", "NFT_emissions": 11})
        LOGGER.info('response: {}'.format(str(response)))
    except Exception as e:
        LOGGER.info('Exception: {}'.format(str(e)))


def test_read_invalid():
    try:
        response = client.post(
            "/store_data",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"NFT_MetaDat"},
        )
    except TypeError as TE:
        LOGGER.info('Exception: {}'.format(str(TE)))
        pass


def test_read_cid():
    cid_str = "bafkreih25basxp4uhk5tz25e7vo7i7efohvepnfyryt6wigxjg6gd7uvea"
    headers = {
        'accept': 'application/json',
    }
    params = {
        'cid': cid_str,
    }

    response = client.get(
        "/cid",
        headers=headers, params=params
    )
    words = response.content.decode().strip('"')
    assert (response.status_code == 200)
    response = requests.get(words)
    assert (response.status_code == 200)


def test_get_seed_invalid_length():
    headers = {
        'accept': 'application/json',
    }
    params = {
        'number_of_words': '13',
    }

    response = client.get(
        "/seed",
        headers=headers, params=params
    )
    assert (response.status_code == 400)


def test_get_seed_12_words():
    headers = {
        'accept': 'application/json',
    }
    params = {
        'number_of_words': '12',
    }

    response = client.get(
        "/seed",
        headers=headers, params=params
    )
    words = response.content.decode()
    words_list = words.split()
    assert (len(words_list) == 12)
    assert (response.status_code == 200)


def test_get_seed_24_words():
    headers = {
        'accept': 'application/json',
    }
    params = {
        'number_of_words': '24',
    }

    response = client.get(
        "/seed",
        headers=headers, params=params
    )

    words = response.content.decode()
    words_list = words.split()
    assert (len(words_list) == 24)
    assert (response.status_code == 200)


def test_get_config():
    headers = {
        'accept': 'application/json',
    }
    response = client.get(
        "/config",
        headers=headers,
    )
    assert (response.status_code == 200)


def test_multihash():
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    json = {"NFT_MetaDat": "mytest", "NFT_emissions": 11}

    response = client.post(
        "/get_ipld_multihash",
        headers=headers,
        json=json
    )
    assert (response.status_code == 200)
