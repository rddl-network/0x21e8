from urllib.error import URLError

from fastapi import APIRouter, HTTPException
from planetmint_driver.exceptions import PlanetmintException

from x21e8.rddl import resolve_nft_cid
from x21e8.wallet.planetmint import resolve_asset_token, create_cid_based_asset
from x21e8.wallet.sw_wallet import SoftwareWallet

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
    responses={404: {"detail": "Not found"}},
)


@router.get("", tags=["Assets"])
async def get_cid_token(cid_token):
    try:
        nft_tx, nft_cid = resolve_asset_token(cid_token)
        nft_data = resolve_nft_cid(nft_cid)
        return {"NFT transaction": nft_tx, "NFT data": nft_data}
    except KeyError as e:
        raise HTTPException(
            status_code=422,
            detail=f"The nft token does not represent a proper NFT: {e.code} : {e.reason}.",
        )
    except URLError as e:
        raise HTTPException(
            status_code=421,
            detail=f"The requested URL could not be resolved: {e.code} : {e.reason}.",
        )


@router.post("", tags=["Assets"])
async def set_cid_token(cid: str):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
    try:
        cid_nft = create_cid_based_asset(cid, wallet)
        return {"cid": cid, "NFT token": cid_nft["id"], "NFT transaction": cid_nft}
    except PlanetmintException as e:
        raise HTTPException(status_code=423, detail="The following exception occurred: {e}.")
