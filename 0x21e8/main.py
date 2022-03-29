from typing import Optional

from fastapi import FastAPI
from model import IssuingRequest, TokenRelatedAccounts, accounts_to_json
from notarize import get_asset_description

import binascii
from planetmint_driver import Planetmint
from planetmint_driver.offchain import fulfill_with_signing_delegation
#from ipld import marshal, multihash
from wallet.liquid import get_liquid_keys, register_asset_id, register_asset_id_on_liquid
from wallet.issue2liquid import issue_tokens
from wallet.planetmint import get_planetmint_keys, get_planetmint_keys_tc

app = FastAPI()

#plntmnt = Planetmint('http://lab.r3c.network:9984')    
plntmnt = Planetmint('https://test.ipdb.io')    
MNEMONIC_PHRASE = "supreme layer police brand month october rather rack proud strike receive joy limit random hill inside brand depend giant success quarter brain butter mechanic"


@app.get("/")
async def root():
    return {"message"}

@app.get("/keypairs")
async def getkeypairs():    
    accounts = TokenRelatedAccounts
    accounts.plpriv , accounts.plpub = get_planetmint_keys( MNEMONIC_PHRASE )
    accounts.plpriv = accounts.plpriv.decode()
    accounts.plpub = accounts.plpub.decode()
    accounts.lqpriv, accounts.lqpub = get_liquid_keys( MNEMONIC_PHRASE )
    return accounts_to_json( accounts )    

@app.post("/issuetokens")
async def issuetokens(issueTokens: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    pl_sk, pl_vk = get_planetmint_keys_tc( MNEMONIC_PHRASE )
    lq_sk, lq_vk = get_liquid_keys( MNEMONIC_PHRASE )

    def pl_signing_function(tx, message):
        import base58
        from nacl.signing import SigningKey

        sk, vk = get_planetmint_keys_tc( MNEMONIC_PHRASE )
        #print(sk.encode(encoding='base58'))
        ncal_sk = SigningKey( base58.b58decode(sk) )
        res = ncal_sk.sign(message).signature
        return res

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
    signed_tx = fulfill_with_signing_delegation( tx,
                                                pl_signing_function)

    token_nft = plntmnt.transactions.send_commit(signed_tx)
    

    # issue tokens
    asset_id = issue_tokens( issueTokens, lq_vk, token_nft['id'], hashed_marshalled)

    # register assets on local node
    register_asset_id( asset_id )
    
    #register assests on liquid
    #register_asset_id_on_liquid( asset_id )
        
    return { "token NFT": token_nft['id'], "signed tx" : signed_tx, "ipdl": hashed_marshalled, "asset_id": asset_id }
