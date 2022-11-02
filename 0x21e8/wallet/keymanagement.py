"""This module provides api for generating mnemonics, seed and deriving keypairs
in bigchaindb-wallet, it does not interface with the wallet keystore.
"""

# TODO normalize mnemonic string
import hashlib
import hmac
import struct
from collections import namedtuple

from mnemonic import Mnemonic
from mnemonic.mnemonic import PBKDF2_ROUNDS
from nacl import secret, utils
from nacl.pwhash import SCRYPT_SALTBYTES as SALTBYTES
from nacl.pwhash import kdf_scryptsalsa208sha256 as kdf
from nacl.signing import SigningKey

HARDENED_INDEX = 0x80000000

ExtendedKey = namedtuple("ExtendedKey", ("privkey", "chaincode"))


SUPPORTED_LANGUAGES = [
    "cinese-simplified",
    "chinese-traditional",
    "english",
    "french",
    "italian",
    "japanese",
    "korean",
    "spanish",
]


def make_mnemonic_phrase(strength=256, language="english", with_entropy=None):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            "{} not found in supported languages: {}".format(
                language, SUPPORTED_LANGUAGES
            )
        )
    mnemonic_obj = Mnemonic(language)
    if with_entropy:
        # TODO check that strength corresponds to entropy length
        mnemonic_phrase = mnemonic_obj.to_mnemonic(with_entropy)
    else:
        mnemonic_phrase = mnemonic_obj.generate(strength=strength)
    return mnemonic_phrase


def mnemonic_to_seed(mnemonic_phrase: str) -> bytes:
    return Mnemonic.to_seed(mnemonic_phrase)


def seed_to_extended_key(seed):
    master_hmac = hmac.new(b"ed25519 seed", digestmod=hashlib.sha512)
    master_hmac.update(seed)
    return ExtendedKey(master_hmac.digest()[:32], master_hmac.digest()[32:])


def derive_key(key: ExtendedKey, tree_index=()):
    privkey, chaincode = key
    for idx in tree_index:
        data = struct.pack("x") + privkey + struct.pack(">I", idx)
        i = hmac.new(chaincode, digestmod=hashlib.sha512)
        i.update(data)
        digest = i.digest()
        privkey = digest[:32]
        chaincode = digest[32:]
    return ExtendedKey(privkey, chaincode)


def path_to_indexes(path):
    assert path.startswith("m")

    def index_to_int(i):
        if i[-1] in "'Hh":
            return int(i[:-1]) + HARDENED_INDEX
        return int(i)

    return tuple(index_to_int(i) for i in path.split("/")[1:])


def derive_from_path(key, path):
    return derive_key(key, path_to_indexes(path))


def privkey_to_pubkey(privkey):
    # PyNaCl uses Ed25519 for digital signatures
    return struct.pack("x") + SigningKey(privkey).verify_key.encode()


def symkey_encrypt(msg, password):
    salt = utils.random(SALTBYTES)
    encrypted = secret.SecretBox(
        kdf(secret.SecretBox.KEY_SIZE, password, salt)
    ).encrypt(msg)
    return encrypted, salt


def symkey_decrypt(key, password, salt):
    return secret.SecretBox(kdf(secret.SecretBox.KEY_SIZE, password, salt)).decrypt(key)
