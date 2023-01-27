from x21e8.model import IssuingRequest, NftAsset


def get_asset_description(issueReq: IssuingRequest, liquid_address, planetmint_address) -> NftAsset:
    return NftAsset(
        name=issueReq.name,
        ticker=issueReq.ticker,
        issued=issueReq.amount,
        precision=issueReq.precision,
        issuer_planetmint=planetmint_address,
        issuer_liquid=liquid_address,
        cid=issueReq.cid,
    )
