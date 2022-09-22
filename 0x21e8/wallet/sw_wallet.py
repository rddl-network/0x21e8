import TrezorCrypto
import wallycore as wally
from nacl.signing import SigningKey
from . import base_wallet
HARDENED = 0x80000000
PLANET_VERSION_PUBLIC = 0x02d41400
PLANET_VERSION_PRIVATE = 0x02d40fc0

class SoftwareWallet(base_wallet.BaseWallet):
    def __init__(self):
        self.seed = None
        self.private_key = None
        self.public_key = None
        self.liquid_address = None
        self._init_wallet()

    def planetmint_sign_digest(self, input, message: bytes):
        ncal_sk = SigningKey(self.private_key)
        res = ncal_sk.sign(message)
        return res.signature  # signature matches signature from other schemes

    def liquid_sign_digest(self, message: bytes):
        pass

    def get_liquid_pubkey(self) -> bytes:
        pass

    def get_liquid_address(self) -> bytes:
        return self.liquid_address

    def get_confidential_liquid_address(self) -> bytes:
        master_blinding_key = wally.asset_blinding_key_from_seed(self.seed)
        script_pubkey = wally.address_to_scriptpubkey(
            self.liquid_address,
            wally.WALLY_NETWORK_LIQUID)
        private_blinding_key = wally.asset_blinding_key_to_ec_private_key(
            master_blinding_key,
            script_pubkey)
        public_blinding_key = wally.ec_public_key_from_private_key(
            private_blinding_key)
        # end-derive_blinding_key

        # start-create_conf_address
        confidential_address = wally.confidential_addr_from_addr(
            self.liquid_address,
            wally.WALLY_CA_PREFIX_LIQUID,
            public_blinding_key)
        return confidential_address
        # end-create_conf_address

    def get_planetmint_pubkey(self) -> bytes:
        return self.public_key

    def _get_planetmint_keys_tc(self):
        node = TrezorCrypto.from_seed(self.seed, TrezorCrypto.ED25519_NAME)
        # [Chain m/0'] check tests/bip32_tests.py for more derivation path examples
        node.derive(HARDENED | 0)
        self.private_key = node.private_key()
        self.public_key = node.public_key()[1:]
        print(self.public_key)

    def _init_wallet(self):
        with open('secret.txt', 'r') as secret:
            self.seed = bytes.fromhex(secret.readline())

        wallet_master_key = wally.bip32_key_from_seed(
            self.seed,
            wally.BIP32_VER_MAIN_PRIVATE, 0)
        wallet_derived_key = wally.bip32_key_from_parent(
            wallet_master_key,
            1,
            wally.BIP32_FLAG_KEY_PRIVATE)
        self.liquid_address = wally.bip32_key_to_address(
            wallet_derived_key,
            wally.WALLY_ADDRESS_TYPE_P2PKH,
            wally.WALLY_ADDRESS_VERSION_P2PKH_LIQUID)
        # end-create_p2pkh_address
        self._get_planetmint_keys_tc()

