from x21e8.application.liquid import LiquidNode
from x21e8.models.transfer import Transfer
from x21e8.utils.cointype import symbol_to_cointype, supported_cointypes
from x21e8.application.planetmint import transfer
from x21e8.wallet.sw_wallet import SoftwareWallet


def token_transfer(transfer_request: Transfer):
    cointype: int = None
    status = 405
    message = "Network ID or Symbol need to be defined"
    if transfer_request.network_slip_id:
        if transfer_request.network_slip_id in supported_cointypes:
            cointype = transfer_request.network_slip_id
        else:
            message = "Network ID or Symbol have to be supported"
    elif transfer_request.network_slip_symbol:
        if symbol_to_cointype(transfer_request.network_slip_symbol):
            cointype = symbol_to_cointype(transfer_request.network_slip_symbol)
        else:
            message = "Network ID or Symbol have to be supported"

    wallet = SoftwareWallet()
    if cointype:
            if cointype == symbol_to_cointype("PLMNT"):
                try:
                # message will be tx if everything was valid
                    status, message = transfer(transfer_request, wallet)
                except Exception as e:
                    status = e.status_code
                    message = e.info["message"]
            elif cointype == symbol_to_cointype("LBTC"):
                try:
                    status, message = LiquidNode().transfer(transfer_request)
                except Exception as e:
                    status = e.status_code
                    message = e.info["message"]
    
    return status, message
