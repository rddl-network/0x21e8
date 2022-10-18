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
    lqpriv: str
    lqpub: str
    plpriv: str
    plpub: str


def accounts_to_json(accounts: TokenRelatedAccounts):
    return {
        "Liquid": {"private": accounts.lqpriv, "public": accounts.lqpub},
        "Planetmint": {"private": accounts.plpriv, "public": accounts.plpub},
    }
