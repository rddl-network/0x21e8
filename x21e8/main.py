from fastapi import FastAPI

from x21e8.routers import assets, data, machine, seed, utils, config

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
app.include_router(config.router)
app.include_router(utils.router)
