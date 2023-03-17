import json
from x21e8.application.liquid import register_asset
from x21e8.config import RDDL_ASSET_REG_ENDPOINT

asset_obj = {
    "asset_id": "838e4fe29789fa6dcacc9f3b38e123682bde8c448572257d0612a22b4a3c03b4",
    "contract": '{"entity":{"domain":"lab.r3c.network"}, "issuer_pubkey":"038951143e74342550a9acdc17c2a2a2bee2d8576104636cbe6432c4e5638cbc7e", "nft":{"token":"470151338e44721ed482e1df2edc9376b6c80c204cfcd1daac5f7e7b73b3ebf0", "ipld":"bafkreifprspd527e46delxm4vbe224rxh7xbh4v3g6ffalvbcjxzjhj644"}, "name":"sufsdfiesfsdssafadf!", "precision":8, "ticker":"TSTMA", "version":0}',
}


def test_register_asset():
    resp = register_asset(
        asset_id=asset_obj["asset_id"],
        contract=json.loads(asset_obj["contract"]),
        registration_endpoint=RDDL_ASSET_REG_ENDPOINT,
    )
    assert resp.status_code == 201


asset_obj_2 = {
    "asset_id": "d32421a6b81bb901d1e2bfabd46b924a67b24b3f2ce853209373eedaba99af73",
    "contract": {
        "entity": {"domain": "lab.r3c.network"},
        "issuer_pubkey": "02a1accfdfb6a3b57442ba3f30d2c1784ac12751a894ea556164d6c5c85bfa3122",
        "nft": {
            "token": "f75c0dad824b83bc59f9f6094f72d7657a3ace7cbd8143e3501c73198a2b0c4f",
            "ipld": "bafkreibebmkz4qkgw6qce56x33h7uf6vy5g7lstskbf2fj7rahvp2t23mm",
        },
        "name": "Tspf4dsfS",
        "precision": 8,
        "ticker": "T4i9O",
        "version": 0,
    },
}

working_json_obj_str = '{"asset_id": "d32421a6b81bb901d1e2bfabd46b924a67b24b3f2ce853209373eedaba99af73","contract":{"entity": {"domain": "lab.r3c.network"}, "issuer_pubkey": "02a1accfdfb6a3b57442ba3f30d2c1784ac12751a894ea556164d6c5c85bfa3122", "nft": {"token": "f75c0dad824b83bc59f9f6094f72d7657a3ace7cbd8143e3501c73198a2b0c4f", "ipld": "bafkreibebmkz4qkgw6qce56x33h7uf6vy5g7lstskbf2fj7rahvp2t23mm"}, "name": "Tspf4dsfS", "precision": 8, "ticker": "T4i9O", "version": 0}}'


def test_string_composition():
    assert (
        f'{{"asset_id": "{asset_obj_2["asset_id"]}","contract":{json.dumps(asset_obj_2["contract"])}}}'
        == working_json_obj_str
    )
