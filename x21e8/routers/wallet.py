from urllib.error import URLError

from fastapi import APIRouter, HTTPException

from x21e8.models.transfer import Transfer
from x21e8.utils.cointype import supported_cointypes, symbol_to_cointype

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"],
    responses={404: {"detail": "Not found"}},
)

@router.post("", tags=["Wallet"])
async def transfer(transfer_request: Transfer):
    cointype: int = None
    if not transfer_request.network_slip_id and not transfer_request.network_slip_symbol:
        return HTTPException(status_code=405, detail="Network ID or Symbol need to be defined")
    elif transfer_request.network_slip_id and transfer_request.network_slip_id in supported_cointypes:
        cointype = transfer_request.network_slip_id 
    elif transfer_request.network_slip_symbol and symbol_to_cointype( transfer_request.network_slip_symbol ):
        cointype = symbol_to_cointype( transfer_request.network_slip_symbol )
    
    if cointype:
        transfer_request.network_slip_id = cointype
        
        
    return
    
    