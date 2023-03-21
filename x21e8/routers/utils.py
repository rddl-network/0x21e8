from fastapi import APIRouter
from fastapi import HTTPException
from x21e8.utils.storage import multi_hash

router = APIRouter(
    prefix="/multihash",
    tags=["Multihash"],
    responses={404: {"detail": "Not found"}},
)


@router.post("", tags=["Multihash"])
async def get_multihash(json_data: dict, encrypt: bool = False):
    try:
        hashed_marshalled = multi_hash(json_data, encrypt)
        return {"cid": hashed_marshalled}
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
