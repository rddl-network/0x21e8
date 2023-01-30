from decouple import config

LQD_RPC_PORT: str = config("LQD_RPC_PORT", default=18886)
LQD_RPC_USER: str = config("LQD_RPC_USER")
LQD_RPC_PASSWORD: str = config("LQD_RPC_PASSWORD")
LQD_RPC_ENDPOINT: str = config("LQD_RPC_ENDPOINT", default="localhost")
LQD_RPC_ENDPOINT_SCHEMA: str = config("LQD_RPC_SCHEMA", default="http")
PLNTMNT_ENDPOINT = config("PLNTMNT_ENDPOINT", default="http://localhost:9984")
WEB3STORAGE_TOKEN = config("WEB3STORAGE_TOKEN")
CID_RESOLVER = config("CID_RESOLVER", default="https://cid-resolver.rddl.io")


def build_liquid_auth_proxy_url():
    return f"{LQD_RPC_ENDPOINT_SCHEMA}://{LQD_RPC_USER}:{LQD_RPC_PASSWORD}@{LQD_RPC_ENDPOINT}:{LQD_RPC_PORT}"


def build_liquid_endpoint_url():
    return f"{LQD_RPC_ENDPOINT_SCHEMA}://{LQD_RPC_ENDPOINT}:{LQD_RPC_PORT}"
