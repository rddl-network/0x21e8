from pydantic import BaseModel

class IssuingRequest(BaseModel):
    name: str
    ticker: str
    amount: int
    precision: int
    public_url: str
    reissue: bool
    cid: str
