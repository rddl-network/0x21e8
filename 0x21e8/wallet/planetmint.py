from mnemonic import Mnemonic
import TrezorCrypto

HARDENED = 0x80000000
PLANET_VERSION_PUBLIC = 0x02d41400
PLANET_VERSION_PRIVATE = 0x02d40fc0


def get_seed() -> bytes:
    mnemonic_obj = Mnemonic("english")
    phrase = mnemonic_obj.generate(256)
    print("New mnemonic phrase: ", phrase)
    seed_bytes = mnemonic_obj.to_seed(phrase, '0x21e8')
    print(f'Seed {seed_bytes.hex()}')
    return seed_bytes


def get_planetmint_keys_tc(seed: bytes):

    node = TrezorCrypto.from_seed(seed, TrezorCrypto.ED25519_NAME)
    # [Chain m/0'] check tests/bip32_tests.py for more derivation path examples
    node.derive(HARDENED | 0)
    print(f"raw private key : {(node.private_key().hex())}")
    print(f"Planetmint chaincode: {node.chain_code().hex()}")
    print(f"planetmint address public: {node.address(PLANET_VERSION_PUBLIC)}")
    print(f"planetmint raw public key: {node.public_key().hex()}")

    print(f"Planetmint private key : {node.serialize_private(PLANET_VERSION_PRIVATE)}")
    print(f"Planetmint public key : {node.serialize_public(PLANET_VERSION_PUBLIC)}")
    signing_key = node.private_key()
    public_key = node.public_key()
    # don't forget stripping the first byte of the public key (01 depicts edwards)
    return signing_key, public_key[1:]
