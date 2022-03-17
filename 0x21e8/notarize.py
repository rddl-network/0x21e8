from model import IssuingRequest
import json

def get_asset_description( issueReq: IssuingRequest, liquid_address, planetmint_address, ipld ):
    nft_asset = {
        'name': issueReq.name,
        'ticker': issueReq.ticker,
        'issued': issueReq.amount,
        'precision': issueReq.precision,
        'issuer_planetmint': planetmint_address,
        'issuer_liquid': liquid_address,
        'ipld': ipld,
        #'asset_proof': "https://lab.r3c.network/.well-knwon/liquid-asset-proof-"+ str(asset_id)
    }
    return {'data': { 'Issued Token' : nft_asset } }

    