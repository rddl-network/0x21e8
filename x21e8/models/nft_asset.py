from pydantic import BaseModel


class NftAsset(BaseModel):
    name: str
    ticker: str
    issued: int
    precision: int
    issuer_planetmint: str
    issuer_liquid: str
    cid: str
