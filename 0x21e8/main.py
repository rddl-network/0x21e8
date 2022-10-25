from dataclasses import dataclass
from model import IssuingRequest
from fastapi import FastAPI, HTTPException

from liquid import issue_tokens
from storage import get_ipfs_link, get_ipfs_file, store_asset, multihashed
from notarize import get_asset_description
from rddl import resolve_nft_cid
from config import LQD_RPC_ENDPOINT, PLNTMNT_ENDPOINT


from wallet.planetmint import create_cid_asset, resolve_asset_token
from wallet.sw_wallet import SoftwareWallet
from wallet.utils import create_and_save_seed, save_seed_from_mnemonic
from urllib.error import URLError

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
async def get_data(cid: str, link2data: bool = False):
    if link2data:
        data = get_ipfs_link(cid)
    else:
        try:
            data = get_ipfs_file(cid)
        except URLError as e:
            raise HTTPException(
                status_code=421, detail=f"The requested URL could not be resolved: { e.code } : { e.reason }."
            )

    return data


@app.get("/cid")
async def resolve_cid_token(cid_token):
    try:
        nft_tx, nft_cid = resolve_asset_token(cid_token)
        nft_data = resolve_nft_cid(nft_cid)
        return {"NFT transaction": nft_tx, "NFT data": nft_data}
    except KeyError as e:
        raise HTTPException(
            status_code=422, detail=f"The nft token does not represent a proper NFT: { e.code } : { e.reason }."
        )
    except URLError as e:
        raise HTTPException(
            status_code=421, detail=f"The requested URL could not be resolved: { e.code } : { e.reason }."
        )


@app.post("/cid")
async def attest_cid(cid: str):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421, detail="The hardware wallet needs to be provisioned by defining a master seed."
        )

    cid_nft = create_cid_asset(cid, wallet)
    return {"cid": cid, "NFT token": cid_nft["id"], "NFT transaction": cid_nft}


@app.post("/machine")
async def attest_machine(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421, detail="The hardware wallet needs to be provisioned by defining a master seed."
        )

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(
        issuing_request_input, wallet.get_liquid_address(), wallet.get_planetmint_pubkey().hex()
    )

    nft_cid = store_asset(nft_asset)
    token_nft = create_cid_asset(nft_cid, wallet)

    # issue tokens
    # asset_id = issue_tokens(issuing_request_input, wallet.get_liquid_address(), token_nft['id'], nft_cid)

    # register assets on local node
    # register_asset_id(asset_id)
    # register_asset_id_on_liquid( asset_id )

    return {"w3storage.cid": nft_cid, "NFT token": token_nft["id"], "NFT transaction": token_nft}


@app.get("/machine")
async def resolve_machine_token_and_data(nft_token: str):
    # get wallet addresses (issuer, private & pub for )

    # create the token NFT - e.g. the token notarization on planetmint
    try:
        nft_tx, nft_cid = resolve_asset_token(nft_token)
        nft_data = resolve_nft_cid(nft_cid, True)
        return {"NFT transaction": nft_tx, "NFT data": nft_data}
    except KeyError as e:
        raise HTTPException(
            status_code=422, detail=f"The nft token does not represent a proper NFT: { e.code } : { e.reason }."
        )
    except URLError as e:
        raise HTTPException(
            status_code=421, detail=f"The requested URL could not be resolved: { e.code } : { e.reason }."
        )


@app.get("/seed")
async def create_seed_and_provision(number_of_words: int):
    if number_of_words == 24:
        strength = 256
    elif number_of_words == 12:
        strength = 128
    else:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")
    return create_and_save_seed(strength)


@app.post("/seed")
async def recover_seed_from_mnemonic(mnemonic_phrase: str):
    word_array = mnemonic_phrase.split()
    size = len(word_array)
    if size not in [12, 24]:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")

    save_seed_from_mnemonic(mnemonic_phrase)


@app.post("/multihash")
async def get_multihash(json_data: dict):
    hashed_marshalled = multihashed(json_data)
    return hashed_marshalled


@app.get("/config")
async def get_configuration():
    config = {
        "planetmint": PLNTMNT_ENDPOINT,
        "liquid": LQD_RPC_ENDPOINT,
    }
    return config
