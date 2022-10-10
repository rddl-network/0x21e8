from model import IssuingRequest
from notarize import get_asset_description
from ipld import marshal, multihash
from wallet.planetmint import attest_planet_mint_nft
from wallet.sw_wallet import SoftwareWallet
from fastapi import FastAPI, HTTPException
from wallet.utils import create_and_save_seed, save_seed_from_mnemonic
from liquid import issue_tokens
app = FastAPI()


@app.post("/attest_machine")
async def issue_planetmint_and_liquid_tokens(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Cryptographic Identity Not Found! Generate one!")

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(issuing_request_input, wallet.get_liquid_address(),
                                      wallet.get_planetmint_pubkey().hex(), issuing_request_input.ipld_hash_hex)

    token_nft = attest_planet_mint_nft(nft_asset, wallet)

    # issue tokens
    asset_id = issue_tokens(issuing_request_input, wallet.get_liquid_address(), token_nft['id'], issuing_request_input.ipld_hash_hex)
    print(asset_id)
    # register assets on local node
    # register_asset_id(asset_id)
    # register_asset_id_on_liquid( asset_id )

    return {"token NFT": token_nft['id'], "token_nft": token_nft, "ipdl": issuing_request_input.ipld_hash_hex}


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


@app.post("/get_ipld_multihash")
async def get_ipld_multihash(json_data: dict):
    marshalled = marshal(json_data)
    hashed_marshalled = multihash(marshalled)
    return hashed_marshalled
