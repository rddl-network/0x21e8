from pydantic import BaseModel
from x21e8.models.issuing_request import IssuingRequest

class NftAsset(BaseModel):
    def __init__(self, issueReq: IssuingRequest, liquid_address, planetmint_address):
        self.name=issueReq.name
        self.ticker=issueReq.ticker
        self.issued=issueReq.amount
        self.precision=issueReq.precision
        self.issuer_planetmint=planetmint_address
        self.issuer_liquid=liquid_address
        self.cid=issueReq.cid
        
    name: str
    ticker: str
    issued: int
    precision: int
    issuer_planetmint: str
    issuer_liquid: str
    cid: str
