import TrezorCrypto

from planetmint_cryptoconditions.crypto import Ed25519SigningKey
from x21e8.network import liquid
from x21e8.wallet.base_wallet import BaseWallet

HARDENED = 0x80000000
PLANET_VERSION_PUBLIC = 0x02D41400
PLANET_VERSION_PRIVATE = 0x02D40FC0


class SoftwareWallet(BaseWallet):
    def __init__(self):
        self.seed = None
        self.private_key = None
        self.public_key = None
        self.planetmint_address = None
        self.liquid_address = None
        self.liquid_derived_key = None
        self._init_wallet()

    def planetmint_sign_digest(self, input, message: bytes):
        cc_key = Ed25519SigningKey( self.private_key, "bytes")
        signature = cc_key.sign( message, encoding="bytes")
        return signature  # signature matches signature from other schemes

    def liquid_sign_digest(self, message: bytes):
        pass

    def get_liquid_pubkey(self) -> bytes:
        return self.liquid_address

    def get_liquid_address(self) -> bytes:
        return self.liquid_address

    def get_confidential_liquid_address(self) -> bytes:
        master_blinding_key = wally.asset_blinding_key_from_seed(self.seed)
        script_pubkey = wally.address_to_scriptpubkey(self.liquid_address, x21e8.network.liquid.WALLY_NETWORK_LIQUID)
        private_blinding_key = wally.asset_blinding_key_to_ec_private_key(master_blinding_key, script_pubkey)
        public_blinding_key = wally.ec_public_key_from_private_key(private_blinding_key)
        # end-derive_blinding_key

        # start-create_conf_address
        confidential_address = wally.confidential_addr_from_addr(
            self.liquid_address, x21e8.network.liquid.WALLY_CA_PREFIX_LIQUID, public_blinding_key
        )
        return confidential_address
        # end-create_conf_address

    def get_planetmint_pubkey(self) -> bytes:
        return self.public_key
    def get_planetmint_address(self) -> str:
        cc_key = Ed25519SigningKey( self.private_key, "bytes")
        encoded_vk = cc_key.get_verifying_key().encode().decode()
        return encoded_vk

    def _get_planetmint_keys_tc(self, id: int):
        self._read_seed()
        node = TrezorCrypto.from_seed(self.seed, TrezorCrypto.ED25519_NAME)
        # [Chain m/0'] check tests/bip32_tests.py for more derivation path examples
        node.derive(HARDENED | 0)
        self.private_key = node.private_key()
        self.public_key = node.public_key()[1:]
        print(self.public_key)

    def _read_seed(self):
        if not self.seed:
            with open("secret.txt", "r") as secret:
                self.seed = bytes.fromhex(secret.readline())

    def derive_liquid_address(self, id: int) -> str:
        self._read_seed()
        master = liquid.liquid_api.ext_key()
        derived_key = liquid.liquid_api.ext_key()
        derivation_path = "m/44h/1h/" + str(id) + "h/0/0"

        liquid.liquid_api.bip32_key_from_seed(
            self.seed, len(self.seed), liquid.VER_TEST_PRIVATE, 0, liquid.liquid_api.byref(master)
        )
        liquid.liquid_api.bip32_key_from_parent_path_str_n(
            master, derivation_path, len(derivation_path), 0, liquid.BIP32_FLAG_KEY_PRIVATE, derived_key
        )
        self.liquid_derived_key = derived_key
        _, derived_key_address = liquid.liquid_api.wally_bip32_key_to_address(
            derived_key, liquid.WALLY_ADDRESS_TYPE_P2PKH, liquid.WALLY_ADDRESS_VERSION_P2PKH_LIQUID_TESTNET
        )
        return derived_key_address

    def make_cbuffer(hex_in):
        from binascii import unhexlify

        if hex_in is None:
            return None, 0
        hex_len = len(hex_in) // 2
        return unhexlify(hex_in), hex_len

    def derive_liquid_private_wif(self, id: int) -> str:
        self._read_seed()
        master = liquid.liquid_api.ext_key()
        derived_key = liquid.liquid_api.ext_key()
        derivation_path = "m/44h/1h/" + str(id) + "h/0/0"

        liquid.liquid_api.bip32_key_from_seed(
            self.seed, len(self.seed), liquid.VER_TEST_PRIVATE, 0, liquid.liquid_api.byref(master)
        )
        _, master_wif = liquid.liquid_api.wally_wif_from_bytes(
            master.priv_key, 32, liquid.WALLY_ADDRESS_VERSION_WIF_TESTNET, liquid.WALLY_WIF_FLAG_COMPRESSED
        )

        liquid.liquid_api.bip32_key_from_parent_path_str_n(
            master, derivation_path, len(derivation_path), 0, liquid.BIP32_FLAG_KEY_PRIVATE, derived_key
        )
        _, derived_key_wif = liquid.liquid_api.wally_wif_from_bytes(
            derived_key.priv_key, 32, liquid.WALLY_ADDRESS_VERSION_WIF_TESTNET, liquid.WALLY_WIF_FLAG_COMPRESSED
        )
        return derived_key_wif

    def _init_wallet(self):
        self.liquid_address = self.derive_liquid_address(0)
        self._get_planetmint_keys_tc(1)
