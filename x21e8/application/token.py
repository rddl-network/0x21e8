
from x21e8.models.transfer import Transfer
from x21e8.utils.cointype import symbol_to_cointype, supported_cointypes
from x21e8.application.planetmint import transfer_planetmint
from x21e8.wallet.sw_wallet import SoftwareWallet


def token_transfer( transfer_request: Transfer ):
    cointype: int = None
    if transfer_request.network_slip_id and transfer_request.network_slip_id in supported_cointypes:
        cointype = transfer_request.network_slip_id 
    elif transfer_request.network_slip_symbol and symbol_to_cointype( transfer_request.network_slip_symbol ):
        cointype = symbol_to_cointype( transfer_request.network_slip_symbol )
        
    tx = None
    wallet = SoftwareWallet()
    status = 405
    message = "Network ID or Symbol need to be defined"
    if cointype and cointype == symbol_to_cointype("PLMNT"):
        try:
            tx = transfer_planetmint( transfer_request, wallet )
        except Exception as e:
            status = e.status_code
            message = e.info['message']
    elif cointype and cointype == symbol_to_cointype("LBTC"):
        # transfer_liquid( transfer_request )
        return
    
    if tx:
        return 200, tx
    else:
        return status, message
