from x21e8.config import PLNTMNT_ENDPOINT, LQD_RPC_HOST
from fastapi import APIRouter

router = APIRouter(
    prefix="/config",
    tags=["Config"],
    responses={404: {"detail": "Not found"}},
)


@router.get("", tags=["Assets"])
async def get_configuration():
    config = {
        "planetmint": PLNTMNT_ENDPOINT,
        "liquid": LQD_RPC_HOST,
    }
    return config
