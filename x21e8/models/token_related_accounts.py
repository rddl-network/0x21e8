from pydantic import BaseModel


class TokenRelatedAccounts(BaseModel):
    lq_priv: str
    lq_pub: str
    pl_priv: str
    pl_pub: str


def accounts_to_json(accounts: TokenRelatedAccounts):
    return {
        "Liquid": {"private": accounts.lq_priv, "public": accounts.lq_pub},
        "Planetmint": {"private": accounts.pl_priv, "public": accounts.pl_pub},
    }
