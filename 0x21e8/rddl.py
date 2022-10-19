from storage import _get_ipfs_link, _get_ipfs_file, store_asset, multihashed


def resolve_nft_cid(cid: str):
    nft_data = _get_ipfs_file(cid)
    try:
        if nft_data["cid"]:
            nft_data["cid_data"] = _get_ipfs_file(nft_data["cid"])
    except KeyError:  # TODO: state that this is not a rddl nft
        raise KeyError
    return nft_data
