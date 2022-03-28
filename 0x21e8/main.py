from typing import Optional

from fastapi import FastAPI
from model import IssuingRequest, TokenRelatedAccounts, accounts_to_json
from notarize import get_asset_description

import binascii
from planetmint_driver import Planetmint
#from ipld import marshal, multihash
from wallet.liquid import get_liquid_keys, register_asset_id, register_asset_id_on_liquid
from wallet.issue2liquid import issue_tokens
from wallet.planetmint import get_planetmint_keys


#plntmnt = Planetmint('http://lab.r3c.network:9984')    
plntmnt = Planetmint('https://test.ipdb.io')    
MNEMONIC_PHRASE = "supreme layer police brand month october rather rack proud strike receive joy limit random hill inside brand depend giant success quarter brain butter mechanic"
app = FastAPI()

@app.get("/")
async def root():
    plntmnt = Planetmint('http://lab.r3c.network:9984')
    sk_raw=Ed25519SigningKey.generate_with_seed(binascii.unhexlify(b'2b4be7f19ee27bbf30c667b642d5f4aa69fd169872f8fc3059c08ebae2eb19e7'))
    my_vk = sk_raw.get_verifying_key().encode(encoding='base58')
    sk = sk_raw.encode(encoding='base58')
    tx = plntmnt.transactions.prepare(
        operation='CREATE',
        signers=my_vk.decode(),
        asset={'data': {'message': 'Blockchain all the things!'}})
    signed_tx = plntmnt.transactions.fulfill( tx, private_keys=sk )
    ret = plntmnt.transactions.send_commit(signed_tx)

    return {"message"}
    

@app.get("/keypairs")
async def getkeypairs():    
    accounts = TokenRelatedAccounts
    accounts.plpriv , accounts.plpub = get_planetmint_keys()
    accounts.plpriv = accounts.plpriv.decode()
    accounts.plpub = accounts.plpub.decode()
    accounts.lqpriv, accounts.lqpub = get_liquid_keys()
    return accounts_to_json( accounts )    

from cryptoconditions.crypto import Ed25519SigningKey, Ed25519VerifyingKey
@app.post("/issuetokens")
async def issuetokens(issueTokens: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    pl_sk, pl_vk = get_planetmint_keys( MNEMONIC_PHRASE )
    lq_sk, lq_vk = get_liquid_keys( MNEMONIC_PHRASE )
    
    

    asset_insurance = { "insurance_contract": "aösjfaölkdjfaoijdfäpowkeßf0iküpfokasüdfpwokfüisajfüoasjfopiajdfüoja" } # random string representing a asset insuring contract
#    marshalled = marshal( asset_insurance )
#    hashed_marshalled = multihash(marshalled)
    hashed_marshalled = "test ipld"

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset=get_asset_description( issueTokens, lq_vk, pl_vk.decode(), hashed_marshalled)
    print(nft_asset)
    tx = plntmnt.transactions.prepare(
        operation='CREATE',
        signers=pl_vk.decode(),
        asset= {'data': { 'Issued Token' : nft_asset}})
    signed_tx = plntmnt.transactions.fulfill( tx, private_keys=pl_sk )
    token_nft = plntmnt.transactions.send_commit(signed_tx)
    

    # issue tokens
    asset_id = issue_tokens( issueTokens, lq_vk, token_nft['id'], hashed_marshalled)

    # register assets on local node
    register_asset_id( asset_id )
    
    #register assests on liquid
    #register_asset_id_on_liquid( asset_id )
        
    return { "token NFT": token_nft['id'], "signed tx" : signed_tx, "ipdl": hashed_marshalled, "asset_id": asset_id }
