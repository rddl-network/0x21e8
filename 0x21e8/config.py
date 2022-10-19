from decouple import config

LQD_RPC_PORT = config('LQD_RPC_PORT', default=18886) 
LQD_RPC_USER = config('LQD_RPC_USER') 
LQD_RPC_PASSWORD = config('LQD_RPC_PASSWORD') 
LQD_RPC_ENDPOINT = config('LQD_RPC_ENDPOINT', default="localhost") 
PLNTMNT_ENDPOINT = config('PLNTMNT_ENDPOINT', default="http://localhost:9984") 