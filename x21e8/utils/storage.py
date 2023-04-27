import json
import urllib3
import w3storage
from urllib.request import urlopen
from multiformats import CID, multihash

from x21e8.config import WEB3STORAGE_TOKEN, CID_RESOLVER
from x21e8.utils.encryption import encrypt_bytes, decrypt_2_bytes

ENCODING = "utf-8"

w3s = w3storage.API(token=WEB3STORAGE_TOKEN)


def marshal(asset: dict):
    # one line json without whitespaces as bytes
    return bytes(json.dumps(asset, separators=(",", ":")), ENCODING)


def unmarshal(marshalled_asset: bytes):
    # unmarshal to dict
    return json.loads(marshalled_asset.decode(ENCODING))


def get_ipfs_link(cid: str):
    return "https://" + cid + ".ipfs.w3s.link"


def register_cid_url(cid: str, url: str):
    http = urllib3.PoolManager()
    cid_resp = http.request(
        "POST", CID_RESOLVER + "/entry?cid=" + cid + "&url=" + url, headers={"Content-Type": "application/json"}
    )
    return cid_resp


def get_ipfs_file(cid: str, decrypt_data: bool = False):
    nft_url = get_ipfs_link(cid)
    marshalled_nft_data = urlopen(nft_url).read()
    print(f"marshalled/encrypted : {marshalled_nft_data}")
    if decrypt_data:
        decrypted_blob = decrypt_2_bytes(marshalled_nft_data)
        print(f"decrypted : {decrypted_blob}")
        nft_data = unmarshal(decrypted_blob)
    else:
        nft_data = unmarshal(marshalled_nft_data)

    return nft_data


def local_marshal(asset: dict, encrypt_data: bool = False):
    marshalled_asset = marshal(asset)
    if not encrypt_data:
        return marshalled_asset
    else:
        return encrypt_bytes(marshalled_asset)


def store_asset(asset: dict, encrypt_data: bool = False):
    marshalled_asset = local_marshal(asset, encrypt_data)
    asset_cid = w3s.post_upload(marshalled_asset)
    register_cid_url(asset_cid, get_ipfs_link(asset_cid))
    return asset_cid


def get_hashed_marshalled(marshalled_asset: bytes):
    hashed_marshalled = CID.decode(multihash.digest(marshalled_asset, "sha2-256"))
    return hashed_marshalled


def get_cid_v1(hashed_marshalled: CID):
    cid = hashed_marshalled.set(base="base32", version=1, codec="raw")
    return cid


def multi_hash(asset: dict, encrypt_data: bool = False):
    marshalled_asset = local_marshal(asset, encrypt_data)
    hashed_marshalled = get_hashed_marshalled(marshalled_asset)
    return str(hashed_marshalled)
