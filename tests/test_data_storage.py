from x21e8.utils.storage import get_ipfs_file, store_asset, register_cid_url


def test_data_storage_float_with_trailing_zero():
    mydata = """{"cid":{"Time": "2023-05-19T15:36:30","ENERGY": {"TotalStartTime":\
"1970-01-01T00:00:00","Total": "102.550","Yesterday": 0.530,\
"Today": 0.344,"Period": 0,"Power": 22,"ApparentPower": 40,"ReactivePower": 33,"Factor": 0.54,\
"Voltage": 229,"Current": 0.174}}}"""

    cid = store_asset(mydata, encrypt_data=False)
    nft_data = get_ipfs_file(cid, decrypt_data=False)
    assert nft_data == mydata


def test_register_cid():
    resp = register_cid_url(
        "bafkreihyvnspnolgisbaz3qqonmcyiuyybvjajzapce5wxfjzgretrazbq",
        "https://bafkreihyvnspnolgisbaz3qqonmcyiuyybvjajzapce5wxfjzgretrazbq.ipfs.w3s.link",
    )
    assert resp.status == 200
