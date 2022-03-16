from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from planetmint_driver import Planetmint
from cryptoconditions.crypto import Ed25519SigningKey, Ed25519VerifyingKey
#from planetmint_driver.crypto import generate_keypair, ed25519_generate_key_pair

from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import binascii

class IssuingRequest(BaseModel):
    name: str
    ticker: str
    amount: int
    precision: int

class TokenRelatedAccounts(BaseModel):
    lq_issuer_address: str
    pl_issuer_address: str
    #lq_initial_beneficemy_vk.verify(b'hello world', sig)ry_addresses: []
    

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
    
    return {"message": ret }


@app.post("/issuetokens")
async def issuetokens(issueTokens: IssuingRequest):
    relAccounts = TokenRelatedAccounts
    relAccounts.lq_issuer_address = "testi1"
    relAccounts.pl_issuer_address = "testi2"
    return {"message": issueTokens, "accounts": [ relAccounts.lq_issuer_address, relAccounts.pl_issuer_address]}
