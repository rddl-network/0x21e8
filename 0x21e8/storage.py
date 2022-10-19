import w3storage
from urllib.request import urlopen
from ipld import marshal, unmarshal

w3s = w3storage.API(
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDdiN0VFMTVlRjk2OTIyZDI1MjA3MkRDQmYzYjFmRDNEOGQzRWI4NTEiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjM4Mzc2OTM0ODQsIm5hbWUiOiJ0ZXN0bmV0LnJkZGwuaW8td2ViLXN0b3JhZ2UifQ.ZunGDj7USRLMU-u43T1qOkRprt_0nbsSJ4fIqmC6AYY"
)


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
