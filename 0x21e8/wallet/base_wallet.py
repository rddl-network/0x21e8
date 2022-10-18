class BaseWallet:
    def save_seed_from_mnemonic(self, mnemonic: str):
        raise NotImplementedError()

    def planetmint_sign_digest(self, input, message: bytes):
        raise NotImplementedError()

    def liquid_sign_digest(self, message: bytes):
        raise NotImplementedError()

    def get_liquid_pubkey(self) -> bytes:
        raise NotImplementedError()

    def get_planetmint_pubkey(self) -> bytes:
        raise NotImplementedError()

    def get_liquid_address(self) -> bytes:
        raise NotImplementedError()

    def get_confidential_liquid_address(self) -> bytes:
        raise NotImplementedError()
