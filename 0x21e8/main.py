from dataclasses import dataclass
from model import IssuingRequest
from notarize import get_asset_description
from ipld import marshal, multihash
from wallet.planetmint import attest_planet_mint_nft
from wallet.sw_wallet import SoftwareWallet
from fastapi import FastAPI, HTTPException
from wallet.utils import create_and_save_seed, save_seed_from_mnemonic
from liquid import issue_tokens
from ipld import marshal, unmarshal
import json
import w3storage
from urllib.request import urlopen

app = FastAPI()
w3s = w3storage.API(token=
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDdiN0VFMTVlRjk2OTIyZDI1MjA3MkRDQmYzYjFmRDNEOGQzRWI4NTEiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjM4Mzc2OTM0ODQsIm5hbWUiOiJ0ZXN0bmV0LnJkZGwuaW8td2ViLXN0b3JhZ2UifQ.ZunGDj7USRLMU-u43T1qOkRprt_0nbsSJ4fIqmC6AYY')

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

def _get_ipfs_link( cid: str ):
    return "https://"+cid+".ipfs.w3s.link"

def _get_ipfs_file( cid:str ):
    nft_url =  _get_ipfs_link(cid)
    marshalled_nft_data = urlopen(nft_url).read()
    nft_data = unmarshal(marshalled_nft_data)
    return nft_data

@app.post("/store_data")
async def store_data( in_data_dict: dict ):
    storage_data = marshal(in_data_dict) 
    cid = w3s.post_upload( storage_data )
    return cid

@app.get("/get_cid_link")
async def get_cid_link( cid ):
    return  _get_ipfs_link(cid)

@app.get("/resolve_nft")
async def resolve_nft( nft_cid: str ):
    nft_data = _get_ipfs_file( nft_cid )
    try:
        if nft_data['cid'] :
            nft_data['cid_data'] = _get_ipfs_file( nft_data['cid'] )
    except KeyError:
        pass
    return nft_data

@app.post("/attest_machine")
async def issue_planetmint_and_liquid_tokens(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cryptographic Identity Not Found! Generate one!")

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(issuing_request_input, wallet.get_liquid_address(),
                                      wallet.get_planetmint_pubkey().hex())
    
    marshalled_nft = marshal(nft_asset)
    nft_cid = w3s.post_upload( marshalled_nft )
    
    token_nft = attest_planet_mint_nft(nft_cid, wallet)

    # issue tokens
    #asset_id = issue_tokens(issuing_request_input, wallet.get_liquid_address(), token_nft['id'], nft_cid)
    
    # register assets on local node
    # register_asset_id(asset_id)
    # register_asset_id_on_liquid( asset_id )

    return { "w3storage.cid": nft_cid, "NFT token": token_nft['id'], "NFT transaction": token_nft }
    

@app.post("/create_seed")
async def create_seed_and_provision(number_of_words: int):
    if number_of_words == 24:
        strength = 256
    elif number_of_words == 12:
        strength = 128
    else:
        raise HTTPException(status_code=400, detail="Mnemonic has to be either 12 or 24 words")
    return create_and_save_seed(strength)


@app.post("/recover_seed_from_mnemonic")
async def recover_seed_from_mnemonic(mnemonic: str):
    save_seed_from_mnemonic(mnemonic)

@app.get("/get/cid_download")
async def get_cid( cid: str ):
    return "https://ipfs.io/ipfs/"+cid

@app.post("/get_ipld_multihash")
async def get_ipld_multihash(json_data: dict):
    marshalled = marshal(json_data)
    hashed_marshalled = multihash(marshalled)
    return hashed_marshalled
