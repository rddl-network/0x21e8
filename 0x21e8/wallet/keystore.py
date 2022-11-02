import json
import os

from base58 import b58decode, b58encode
from bigchaindb_driver.crypto import generate_keypair
from mnemonic import Mnemonic
from mnemonic.mnemonic import PBKDF2_ROUNDS

from bigchaindb_wallet.keymanagement import (
    ExtendedKey,
    derive_from_path,
    privkey_to_pubkey,
    symkey_decrypt,
    symkey_encrypt,
)

PLANETMINT_COINTYPE = 8680
PLNTMNTW_TREE_INDEX_ROOT = (44, PLANETMINT_COINTYPE)
PLNTMNTW_PATH_TEMPLATE = "m/44/{cointype}'/{{account}}'/0/{{address_index}}'".format(
    cointype=PLANETMINT_COINTYPE
)
DEFAULT_KEYSTORE_FILENAME = ".plntmnt_wallet"


class WalletError(Exception):
    """Exceptions safe to show in output."""


def bdbw_derive_account(key: ExtendedKey, account, index=0):
    return derive_from_path(
        key, PLNTMNTW_PATH_TEMPLATE.format(account=account, address_index=index)
    )


def wallet_dumps(wallet_dict):
    return json.dumps(wallet_dict, sort_keys=True, indent=4)


def wallet_dump(wallet_dict, file_location):
    # XXX check whether wallet already exist XXX
    with open(file_location, "w") as f:
        f.write(wallet_dumps(wallet_dict))


def _get_wallet_account(wallet_dict, wallet_name):
    try:
        return wallet_dict[wallet_name]
    except KeyError:
        raise WalletError("Account {} is not found".format(wallet_name))


def get_master_xprivkey(wallet_dict, wallet_name: str, password: str) -> str:
    wallet = _get_wallet_account(wallet_dict, wallet_name)
    try:
        chaincode = bytes.fromhex(wallet["chain_code"])
        master_privkey = wallet["master_privkey"]
        privkey = symkey_decrypt(
            bytes.fromhex(master_privkey["key"]),
            password.encode(),
            bytes.fromhex(master_privkey["salt"]),
        )
        return ExtendedKey(privkey, chaincode)
    except KeyError:
        raise WalletError("Account {} contains errors".format(wallet_name))


def make_wallet_dict(master_xkey: ExtendedKey, password, name="default"):
    def _value_encode(val):
        return val.hex()

    master_privkey_crypt, salt = symkey_encrypt(
        master_xkey.privkey,
        password.encode(),
    )
    return {
        name: {
            "chain_code": _value_encode(master_xkey.chaincode),
            "master_pubkey": _value_encode(privkey_to_pubkey(master_xkey.privkey)),
            "master_privkey": {
                "format": "cryptsalsa208sha256base58",
                "salt": _value_encode(salt),
                "key": _value_encode(master_privkey_crypt),
            },
        }
    }


def get_home_path_and_warn():
    home_path = os.environ.get("HOME")
    if home_path is None:
        home_path = "."  # TODO warn
    return home_path


def get_wallet_content():
    try:
        # TODO convert to Path object
        location = "{}/{}".format(get_home_path_and_warn(), DEFAULT_KEYSTORE_FILENAME)
        with open(location) as f:
            return json.loads(f.read())
    except OSError:
        raise WalletError("Wallet not found")


def get_private_key_drv(name, address, index, password):
    wallet_dict = get_wallet_content()
    privkey = get_master_xprivkey(wallet_dict, name, password)
    return bdbw_derive_account(privkey, address, index)


def get_public_key_drv(name, address, index, password):
    wallet_cont = get_wallet_content()
    privkey = get_master_xprivkey(wallet_cont, name, password)
    return bdbw_derive_account(privkey, address, index)
