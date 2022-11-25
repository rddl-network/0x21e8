from .model import IssuingRequest


def get_asset_description(issueReq: IssuingRequest, liquid_address, planetmint_address):

    nft_asset = {
        "name": issueReq.name,
        "ticker": issueReq.ticker,
        "issued": issueReq.amount,
        "precision": issueReq.precision,
        "issuer_planetmint": planetmint_address,
        "issuer_liquid": liquid_address,
        "cid": issueReq.cid,
        #'asset_proof': "https://lab.r3c.network/.well-knwon/liquid-asset-proof-"+ str(asset_id)
    }
    return nft_asset
