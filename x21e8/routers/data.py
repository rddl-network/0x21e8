from urllib.error import URLError
from fastapi import APIRouter, HTTPException
from x21e8.lib.storage import get_ipfs_link, get_ipfs_file, store_asset

router = APIRouter(
    prefix="/data",
    tags=["Data"],
    responses={404: {"detail": "Not found"}},
)


@router.post("", tags=["Data"])
async def set_data(in_data_dict: dict, encrypt: bool = False):
    try:
        cid = store_asset(in_data_dict, encrypt_data=encrypt)
        return {"cid": cid}
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )


@router.get("", tags=["Data"])
async def get_data(cid: str, link2data: bool = False, decrypt: bool = False):
    if link2data:
        data = get_ipfs_link(cid)
    else:
        try:
            data = get_ipfs_file(cid, decrypt)
        except URLError as e:
            raise HTTPException(
                status_code=421,
                detail=f"The requested URL could not be resolved: {e.code} : {e.reason}.",
            )

    return {"cid": data}
