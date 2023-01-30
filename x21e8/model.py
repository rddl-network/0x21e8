from pydantic import BaseModel


class IssuingRequest(BaseModel):
    name: str
    ticker: str
    amount: int
    precision: int
    public_url: str
    reissue: bool
    cid: str


class TokenRelatedAccounts(BaseModel):
    lq_priv: str
    lq_pub: str
    pl_priv: str
    pl_pub: str


class NftAsset(BaseModel):
    name: str
    ticker: str
    issued: int
    precision: int
    issuer_planetmint: str
    issuer_liquid: str
    cid: str


def accounts_to_json(accounts: TokenRelatedAccounts):
    return {
        "Liquid": {"private": accounts.lq_priv, "public": accounts.lq_pub},
        "Planetmint": {"private": accounts.pl_priv, "public": accounts.pl_pub},
    }
