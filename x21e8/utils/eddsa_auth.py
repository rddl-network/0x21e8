import urllib3
import hashlib
from x21e8.config import RDDL_AUTH
from x21e8.wallet.sw_wallet import SoftwareWallet


def compute_hash(challenge):
    byte_string = bytes(challenge, "utf-8")
    hash_local = hashlib.sha256()
    hash_local.update(byte_string)
    return hash_local.digest()


def get_jwt_token():
    http = urllib3.PoolManager()
    wallet = SoftwareWallet()
    public_key = wallet.get_planetmint_address()
    get_challenge_response = http.request(
        "GET", RDDL_AUTH + f"/auth/?public_key={public_key}", headers={"Content-Type": "application/json"}
    )
    if get_challenge_response.status != 200:
        return ""
    challenge = get_challenge_response.json()["challenge"]
    hashed_challenge = compute_hash(challenge)
    signature = wallet.planetmint_sign_challenge(challenge=hashed_challenge)

    jwt_response = http.request(
        "POST",
        RDDL_AUTH + f"/auth/?public_key={public_key}&signature={signature.decode()}",
        headers={"Content-Type": "application/json"},
    )
    if jwt_response.status != 200:
        return ""
    return jwt_response.json()["access_token"]
