import requests
from urllib.error import URLError
from fastapi import FastAPI, HTTPException
from planetmint_driver.exceptions import PlanetmintException

from x21e8.model import IssuingRequest
from x21e8.liquid import issue_tokens
from x21e8.routers import assets, data, machine, seed
from x21e8.storage import store_asset, multi_hash
from x21e8.notarize import get_asset_description
from x21e8.rddl import resolve_nft_cid
from x21e8.config import LQD_RPC_ENDPOINT, PLNTMNT_ENDPOINT, build_liquid_endpoint_url

from x21e8.wallet.planetmint import create_cid_based_asset, resolve_asset_token
from x21e8.wallet.sw_wallet import SoftwareWallet
from x21e8.wallet.utils import create_and_save_seed, save_seed_from_mnemonic

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

app.include_router(assets.router)
app.include_router(data.router)
app.include_router(machine.router)
app.include_router(seed.router)


@app.post("/multihash")
async def get_multihash(json_data: dict, encrypt: bool = False):
    try:
        hashed_marshalled = multi_hash(json_data, encrypt)
        return {"cid": hashed_marshalled}
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
