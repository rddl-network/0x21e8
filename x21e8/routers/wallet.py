from urllib.error import URLError

from fastapi import APIRouter, HTTPException

from x21e8.models.transfer import Transfer
from x21e8.application.token import token_transfer
from x21e8.wallet.sw_wallet import SoftwareWallet

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"],
    responses={404: {"detail": "Not found"}},
)

@router.get("", tags=["Wallet addresses"])
async def get_addresses():
    try:
        wallet = SoftwareWallet()
        liquid_address = wallet.get_liquid_address()
        planemint_address = wallet.get_planetmint_address()
        return { "liquid address": liquid_address, "planetmint address": planemint_address}
    except Exception as e:
        raise HTTPException(status_code=427, detail=e)



@router.post("", tags=["Wallet"])
async def transfer(transfer_request: Transfer):
    status, details = token_transfer(transfer_request)
    if status >= 400:
        return HTTPException(status_code=status, detail=details)
    else:
        return details
