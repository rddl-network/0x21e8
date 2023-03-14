from decouple import config

LQD_RPC_PORT: str = config("LQD_RPC_PORT", default=18891)
LQD_RPC_USER: str = config("LQD_RPC_USER", default="user")
LQD_RPC_PASSWORD: str = config("LQD_RPC_PASSWORD", default="password")
LQD_RPC_HOST: str = config("LQD_RPC_HOST", default="localhost")
LQD_RPC_ENDPOINT_SCHEMA: str = config("LQD_RPC_SCHEMA", default="http")
PLNTMNT_ENDPOINT = config("PLNTMNT_ENDPOINT", default="http://localhost:9984")
WEB3STORAGE_TOKEN = config("WEB3STORAGE_TOKEN")
CID_RESOLVER = config("CID_RESOLVER", default="https://cid-resolver.rddl.io")
RDDL_ASSET_REG_ENDPOINT = config("RDDL_ASSET_REG_ENDPOINT", default="http://lab.r3c.network:8090/register_asset")
LIQUID_REGISTRATION_DOMAIN = config("LIQUID_REGISTRATION_DOMAIN", default="lab.r3c.network")
LIQUID_ASSET_REG_ENDPOINT = config( "LIQUID_ASSET_REG_ENDPOINT", default="https://assets-testnet.blockstream.info/")
