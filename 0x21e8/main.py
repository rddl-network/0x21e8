from model import IssuingRequest
from fastapi import FastAPI, HTTPException
import requests

from liquid import issue_tokens
from storage import get_ipfs_link, get_ipfs_file, store_asset, multihashed
from notarize import get_asset_description
from rddl import resolve_nft_cid
from config import LQD_RPC_ENDPOINT, PLNTMNT_ENDPOINT

from wallet.planetmint import create_cid_based_asset, resolve_asset_token
from wallet.sw_wallet import SoftwareWallet
from wallet.utils import create_and_save_seed, save_seed_from_mnemonic
from urllib.error import URLError

from planetmint_driver.exceptions import PlanetmintException

tags_metadata = [
    {
        "name": "Data",
        "description": "Stores dictionary data to IPFS and returns the CID.",
    },
    {
        "name": "Assets",
        "description": "Notarizes a given asset defined by its CID on Planetmint and resolves a given Token representing an assets CID.",
    },
    {
        "name": "Machines",
        "description": "Resolves the NFT and attests new machines via CID content and returns the content",
    },
    {
        "name": "Seed",
        "description": "Creates random seeds and returns mnemonic phrases for backups and let recover from backups.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.post("/data", tags=["Data"])
async def set_data(in_data_dict: dict, encrypt: bool = False):
    try:
        cid = store_asset(in_data_dict, encrypt_data=encrypt)
        return cid
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )


@app.get("/data", tags=["Data"])
async def get_data(cid: str, link2data: bool = False, decrypt: bool = False):
    if link2data:
        data = get_ipfs_link(cid)
    else:
        try:
            data = get_ipfs_file(cid, decrypt)
        except URLError as e:
            raise HTTPException(
                status_code=421,
                detail=f"The requested URL could not be resolved: { e.code } : { e.reason }.",
            )

    return data


@app.get("/cid", tags=["Assets"])
async def get_cid_token(cid_token):
    try:
        nft_tx, nft_cid = resolve_asset_token(cid_token)
        nft_data = resolve_nft_cid(nft_cid)
        return {"NFT transaction": nft_tx, "NFT data": nft_data}
    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"The nft token does not represent a proper NFT: { e.code } : { e.reason }.",
        )
    except URLError as e:
        raise HTTPException(
            status_code=421,
            detail=f"The requested URL could not be resolved: { e.code } : { e.reason }.",
        )


@app.post("/cid", tags=["Assets"])
async def set_cid_token(cid: str):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
    try:
        cid_nft = create_cid_based_asset(cid, wallet)
        return {"cid": cid, "NFT token": cid_nft["id"], "NFT transaction": cid_nft}
    except PlanetmintException as e :
        raise HTTPException(
            status_code=423,
            detail="The Planetmint server configured does not support the given transaction schema."
        )


@app.post("/machine", tags=["Machines"])
async def set_machine(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(
        issuing_request_input,
        wallet.get_liquid_address(),
        wallet.get_planetmint_pubkey().hex(),
    )
    try:
        nft_cid = store_asset(nft_asset)
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
    try:
        token_nft = create_cid_based_asset(nft_cid, wallet)
    except PlanetmintException as e :
        raise HTTPException(
            status_code=423,
            detail="The Planetmint server configured does not support the given transaction schema."
        )

    # issue tokens
    asset_id, contract = None, None
    try:
        asset_id, contract = issue_tokens(issuing_request_input, wallet.get_liquid_address(), token_nft["id"], nft_cid)
    except Exception as e:
        print(e)
    # register assets on r3c node

    try:
        response = requests.post(
            "http://lab.r3c.network:8090/register_asset",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"asset_id": asset_id, "contract": contract},
        )
    except Exception as e:
        print(e)

    return {
        "w3storage.cid": nft_cid,
        "NFT token": token_nft["id"],
        "NFT transaction": token_nft,
    }


@app.get("/machine", tags=["Machines"])
async def get_machine(nft_token: str):
    # get wallet addresses (issuer, private & pub for )

    # create the token NFT - e.g. the token notarization on planetmint
    try:
        nft_tx, nft_cid = resolve_asset_token(nft_token)
        nft_data = resolve_nft_cid(nft_cid, True)
        return {"NFT transaction": nft_tx, "NFT data": nft_data}
    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"The nft token does not represent a proper NFT: { e.code } : { e.reason }.",
        )
    except URLError as e:
        raise HTTPException(
            status_code=421,
            detail=f"The requested URL could not be resolved: { e.code } : { e.reason }.",
        )


@app.get("/seed", tags=["Seed"])
async def create_seed_and_provision(number_of_words: int):
    if number_of_words == 24:
        strength = 256
    elif number_of_words == 12:
        strength = 128
    else:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")
    return create_and_save_seed(strength)


@app.post("/seed", tags=["Seed"])
async def recover_seed_from_mnemonic(mnemonic_phrase: str):
    word_array = mnemonic_phrase.split()
    size = len(word_array)
    if size not in [12, 24]:
        raise HTTPException(status_code=420, detail="A mnemonic has to contain 12 or 24 words")

    save_seed_from_mnemonic(mnemonic_phrase)


@app.post("/multihash")
async def get_multihash(json_data: dict, encrypt: bool = False):
    try:
        hashed_marshalled = multihashed(json_data, encrypt)
        return hashed_marshalled
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )


@app.get("/config")
async def get_configuration():
    config = {
        "planetmint": PLNTMNT_ENDPOINT,
        "liquid": LQD_RPC_ENDPOINT,
    }
    return config
