
_symbol2cointype  = {
    "LBTC": 998,
    "PLMNT": 8680,
}

supported_cointypes = [ 998, 8680, ]

def symbol_to_cointype( symbol: str ) -> int:
    if symbol in _symbol2cointype:
        return _symbol2cointype[symbol]
    else:
        return None
    