from pydantic import BaseModel


class Transfer(BaseModel):
    network_slip_symbol: str
    network_slip_id: int
    account: int  # defaults to 0
    change: int  # defaults to 0
    index: int  # defaults to 0
    token_id: str  # tx-id on planetmint, asset-id on liquid
    output_id: int  # planetmint specific (to identify UTXO), unused on Liquid
    amount: float  # only integers for planetmint, floats otherwise
    recipient: str
    is_confidential: bool  # only supported on liquid
