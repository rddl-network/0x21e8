from urllib.error import URLError

from fastapi import APIRouter, HTTPException

from x21e8.models.transfer import Transfer
from x21e8.utils.cointype import supported_cointypes, symbol_to_cointype
from x21e8.application.token import token_transfer

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"],
    responses={404: {"detail": "Not found"}},
)


@router.post("", tags=["Wallet"])
async def transfer(transfer_request: Transfer):
    status, details = token_transfer(transfer_request)
    if status >= 400:
        return HTTPException(status_code=status, detail=details)
    else:
        return details
