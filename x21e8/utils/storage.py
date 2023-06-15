import urllib3
import w3storage
from urllib.request import urlopen
from multiformats import CID, multihash
from x21e8.utils.eddsa_auth import get_jwt_token
from x21e8.config import WEB3STORAGE_TOKEN, CID_RESOLVER
from x21e8.utils.encryption import encrypt_bytes, decrypt_2_bytes

ENCODING = "utf-8"

w3s = w3storage.API(token=WEB3STORAGE_TOKEN)


def get_ipfs_link(cid: str):
    return "https://" + cid + ".ipfs.w3s.link"


def register_cid_url(cid: str, url: str):
    http = urllib3.PoolManager()
    token = get_jwt_token()
    headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": f"Bearer {token}"}
    url = CID_RESOLVER + "/entry/?cid=" + cid + "&url=" + url
    cid_resp = http.request( "POST", url, headers=headers )
    return cid_resp


def decryption_layer(data, decrypt_data: bool = False):
    if decrypt_data:
        print(f"encrypted : {data}")
        decrypted_blob = decrypt_2_bytes(data)
        print(f"decrypted : {decrypted_blob.decode()}")
        data = decrypted_blob
    else:
        print(f"data : '{data.decode()}'")

    return data.decode()


def get_ipfs_file(cid: str, decrypt_data: bool = False):
    nft_url = get_ipfs_link(cid)
    nft_data = urlopen(nft_url).read()
    return decryption_layer(nft_data, decrypt_data)


def encryption_layer(asset: str, encrypt_data: bool = False):
    if not encrypt_data:
        return asset
    else:
        return encrypt_bytes(bytes(asset, "utf-8"))


def store_asset(asset: str, encrypt_data: bool = False):
    marshalled_asset = encryption_layer(asset, encrypt_data)
    asset_cid = w3s.post_upload(marshalled_asset)
    register_cid_url(asset_cid, get_ipfs_link(asset_cid))
    return asset_cid


def get_hashed_marshalled(asset: str):
    asset_bytes = bytes(asset, "utf-8")
    hashed_marshalled = CID.decode(multihash.digest(asset_bytes, "sha2-256"))
    return hashed_marshalled


def get_cid_v1(hashed_marshalled: CID):
    cid = hashed_marshalled.set(base="base32", version=1, codec="raw")
    return cid


def multi_hash(asset: dict, encrypt_data: bool = False):
    marshalled_asset = encryption_layer(asset, encrypt_data)
    hashed_marshalled = get_hashed_marshalled(marshalled_asset)
    return str(hashed_marshalled)


def calculate_cid_v1(asset: str):
    hashed_asset = get_hashed_marshalled(asset)
    cid = get_cid_v1(hashed_asset)
    return str(cid)
