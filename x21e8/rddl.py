from .storage import get_ipfs_file


def resolve_nft_cid(cid: str, machine_nft_cid: bool = False):
    nft_data = get_ipfs_file(cid)
    if machine_nft_cid:
        try:
            if nft_data["cid"]:
                nft_data["cid_data"] = get_ipfs_file(nft_data["cid"])
        except KeyError:  # TODO: state that this is not a rddl nft
            raise KeyError
    return nft_data
