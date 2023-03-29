from x21e8.models.transfer import Transfer
from x21e8.utils.cointype import symbol_to_cointype, supported_cointypes
from x21e8.application.planetmint import transfer_planetmint
from x21e8.wallet.sw_wallet import SoftwareWallet


def token_transfer(transfer_request: Transfer):
    tx = None
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

    if cointype and cointype == symbol_to_cointype("PLMNT"):
        try:
            status, message = transfer_planetmint(transfer_request, wallet)
        except Exception as e:
            status = e.status_code
            message = e.info["message"]
    elif cointype and cointype == symbol_to_cointype("LBTC"):
        # transfer_liquid( transfer_request )
        return

    return status, message
