from fastapi import FastAPI, HTTPException

from x21e8.routers import assets, data, machine, seed
from x21e8.storage import multi_hash
from x21e8.config import LQD_RPC_HOST, PLNTMNT_ENDPOINT


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
        "liquid": LQD_RPC_HOST,
    }
    return config
