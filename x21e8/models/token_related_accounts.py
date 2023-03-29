from pydantic import BaseModel


class TokenRelatedAccounts(BaseModel):
    lq_priv: str
    lq_pub: str
    pl_priv: str
    pl_pub: str

    def accounts_to_json(self) -> dict:
        return {
            "Liquid": {"private": self.lq_priv, "public": self.lq_pub},
            "Planetmint": {"private": self.pl_priv, "public": self.pl_pub},
        }
