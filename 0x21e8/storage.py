import w3storage
from urllib.request import urlopen
from ipld import marshal, unmarshal, multihash
from config import WEB3STORAGE_TOKEN



w3s = w3storage.API(token=WEB3STORAGE_TOKEN)


def _get_ipfs_link(cid: str):
    return "https://" + cid + ".ipfs.w3s.link"


def _get_ipfs_file(cid: str):
    nft_url = _get_ipfs_link(cid)
    marshalled_nft_data = urlopen(nft_url).read()
    nft_data = unmarshal(marshalled_nft_data)
    return nft_data


def store_asset(asset: dict):
    marshalled_asset = marshal(asset)
    asset_cid = w3s.post_upload(marshalled_asset)
    return asset_cid


def multihashed(asset: dict):
    marshalled = marshal(asset)
    hashed_marshalled = multihash(marshalled)
    return hashed_marshalled
