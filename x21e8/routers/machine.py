from urllib.error import URLError

from fastapi import APIRouter, HTTPException, requests
from planetmint_driver.exceptions import PlanetmintException

from x21e8.config import get_liquid_endpoint_url
from x21e8.liquid import issue_tokens
from x21e8.model import IssuingRequest
from x21e8.notarize import get_asset_description
from x21e8.rddl import resolve_nft_cid
from x21e8.storage import store_asset
from x21e8.wallet.planetmint import create_cid_based_asset, resolve_asset_token
from x21e8.wallet.sw_wallet import SoftwareWallet

router = APIRouter(
    prefix="/machine",
    tags=["Machines"],
    responses={404: {"detail": "Not found"}},
)


@router.post("", tags=["Machines"])
async def set_machine(issuing_request_input: IssuingRequest):
    # get wallet addresses (issuer, private & pub for )
    try:
        wallet = SoftwareWallet()
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = get_asset_description(
        issuing_request_input,
        wallet.get_liquid_address(),
        wallet.get_planetmint_pubkey().hex(),
    )
    try:
        nft_cid = store_asset(nft_asset)
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
    try:
        token_nft = create_cid_based_asset(nft_cid, wallet)
    except PlanetmintException as e:
        raise HTTPException(
            status_code=423, detail="The Planetmint server configured does not support the given transaction schema."
        )

    if check_if_tokens_should_be_issued(issuing_request_input):
        # issue tokens
        asset_id, contract = None, None
        try:
            asset_id, contract = issue_tokens(issuing_request_input, token_nft["id"], nft_cid)
        except Exception as e:
            print(e)
        # register assets on r3c node

        try:
            response = requests.post(
                f"{get_liquid_endpoint_url}/register_asset",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                json={"asset_id": asset_id, "contract": contract},
            )
        except Exception as e:
            print(e)

    return {
        "w3storage.cid": nft_cid,
        "NFT token": token_nft["id"],
        "NFT transaction": token_nft,
    }


def check_if_tokens_should_be_issued(issuing_request: IssuingRequest) -> bool:
    return not (issuing_request.amount == 0 and issuing_request.ticker == "")


@router.get("", tags=["Machines"])
async def get_machine(nft_token: str):
    # get wallet addresses (issuer, private & pub for )

    # create the token NFT - e.g. the token notarization on planetmint
    try:
        nft_tx, nft_cid = resolve_asset_token(nft_token)
        nft_data = resolve_nft_cid(nft_cid, True)
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
