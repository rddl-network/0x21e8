from urllib.error import URLError

from fastapi import APIRouter, HTTPException
from planetmint_driver.exceptions import PlanetmintException


from x21e8.application.liquid import LiquidNode
from x21e8.config import RDDL_ASSET_REG_ENDPOINT
from x21e8.models.issuing_request import IssuingRequest
from x21e8.models.nft_asset import NftAsset
from x21e8.application.rddl import resolve_nft_cid
from x21e8.utils.storage import store_asset
from x21e8.application.planetmint import create_cid_based_asset, resolve_asset_token
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
        wif_key = wallet.derive_liquid_private_wif(0)
        LiquidNode().inject_key_into_liquid(wif_key)
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )

    # create the token NFT - e.g. the token notarization on planetmint
    nft_asset = NftAsset(
        name=issuing_request_input.name,
        ticker=issuing_request_input.ticker,
        issued=issuing_request_input.amount,
        precision=issuing_request_input.precision,
        issuer_planetmint=wallet.get_planetmint_pubkey().hex(),
        issuer_liquid=wallet.get_liquid_address(),
        cid=issuing_request_input.cid,
    )
    try:
        nft_cid = store_asset(str(nft_asset.__dict__))
    except FileNotFoundError:
        raise HTTPException(
            status_code=421,
            detail="The hardware wallet needs to be provisioned by defining a master seed.",
        )
    try:
        token_nft = create_cid_based_asset(nft_cid, wallet)
    except PlanetmintException as e:
        print(f"The Planetmint server configured does not support the given transaction. {e}")
        raise HTTPException(
            status_code=423,
            detail=f"The Planetmint server configured does not support the given transaction. {e}",
        )

    if check_if_tokens_should_be_issued(issuing_request_input):
        asset, asset_id, contract = LiquidNode().issue_tokens(issuing_request_input, token_nft["id"], nft_cid)
        print(f"Liquid issued token: {asset_id}  - {contract}")
        try:
            response = LiquidNode.register_asset(asset, contract, RDDL_ASSET_REG_ENDPOINT)
            print(f"RDDL asset registration: {response}")
        except Exception as e:
            print(f"Exception: RDDL asset registration - {e}")
            raise HTTPException(status_code=425, detail=f"Exception: RDDL asset registration - {e}")

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
