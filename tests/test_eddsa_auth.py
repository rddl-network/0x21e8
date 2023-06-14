from x21e8.utils.eddsa_auth import get_jwt_token


def test_get_jwt_token():
    token_resp = get_jwt_token()
    assert token_resp != ""
