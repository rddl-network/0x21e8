from dataclasses import dataclass
from model import IssuingRequest
from notarize import get_asset_description
from wallet.planetmint import attest_cid, PLNTMNT_ENDPOINT
from wallet.sw_wallet import SoftwareWallet
from fastapi import FastAPI, HTTPException
from wallet.utils import create_and_save_seed, save_seed_from_mnemonic
from liquid import issue_tokens, LQD_ENDPOINT
from storage import _get_ipfs_link, _get_ipfs_file, store_asset, multihashed
from urllib.request import urlopen

app = FastAPI()

tags_metadata = [
    {
        "name": "store_data",
        "description": "Stores dictionary data to IPFS and returns the CID.",
    },
    {
        "name": "get_cid_link",
        "description": "Gets the URI for a given CID on IPFS.",
    },
    {
        "name": "resolve_nft",
        "description": "Resolves the NFT CID and the CID content and returns the content",
    },
    {
        "name": "get_data_linke",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
    {
        "name": "get_data_linke",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]


@app.post("/data")
async def store_data(in_data_dict: dict):
    cid = store_asset(in_data_dict)
    return cid


@app.get("/data")
async def resolve_nft(cid: str):
    data = _get_ipfs_file(cid)
    return data


@app.get("/nft")
async def resolve_nft(nft_cid: str):
    nft_data = _get_ipfs_file(nft_cid)
    try:
        if nft_data["cid"]:
            nft_data["cid_data"] = _get_ipfs_file(nft_data["cid"])
    except KeyError:
        pass
    return nft_data


@app.get("/cid")
async def get_cid_link(cid):
    return _get_ipfs_link(cid)


@app.post("/cid")
async def attest_cid_on_planetmint(cid: str):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cryptographic Identity Not Found! Generate one!")

    cid_nft = attest_cid(cid, wallet)
    return {"cid": cid, "NFT token": cid_nft["id"], "NFT transaction": cid_nft}


@app.post("/machine")
async def issue_planetmint_and_liquid_tokens(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cryptographic Identity Not Found! Generate one!")

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(
        issuing_request_input, wallet.get_liquid_address(), wallet.get_planetmint_pubkey().hex()
    )

    nft_cid = store_asset(nft_asset)
    token_nft = attest_cid(nft_cid, wallet)

    # issue tokens
    # asset_id = issue_tokens(issuing_request_input, wallet.get_liquid_address(), token_nft['id'], nft_cid)

    # register assets on local node
    # register_asset_id(asset_id)
    # register_asset_id_on_liquid( asset_id )

    return {"w3storage.cid": nft_cid, "NFT token": token_nft["id"], "NFT transaction": token_nft}


@app.get("/seed")
async def create_seed_and_provision(number_of_words: int):
    if number_of_words == 24:
        strength = 256
    elif number_of_words == 12:
        strength = 128
    else:
        raise HTTPException(status_code=400, detail="Mnemonic has to be either 12 or 24 words")
    return create_and_save_seed(strength)


@app.post("/seed")
async def recover_seed_from_mnemonic(mnemonic: str):
    save_seed_from_mnemonic(mnemonic)


@app.post("/get_ipld_multihash")
async def get_ipld_multihash(json_data: dict):
    hashed_marshalled = multihashed(json_data)
    return hashed_marshalled


@app.get("/config")
async def get_configuration():
    config = {
        "planetmint": PLNTMNT_ENDPOINT,
        "liquid": LQD_ENDPOINT,
    }
    return config
