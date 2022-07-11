from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
import paramiko
import binascii

"""setup('liquidv1')

sk = PrivateKey()

address = sk.get_public_key().get_address()
print(F"Public key: {address.to_string()}")
print("")
print(F"Private key: {sk.to_wif()}")
"""

"""
Public key: H65oVENr7HMigQAUjTzjuYQ5DVwCgwk1Qr
Private key: L16DiAf7jTcNuDa8cuj5HagRAZ8ECc2xbda9y6o2NLERiVtuft7L
"""
import os
import wallycore as wally

def get_liquid_keys( mnemonic ) :

    # start-create_p2pkh_address
    _, seed = wally.bip39_mnemonic_to_seed512(mnemonic, '')
    wallet_master_key = wally.bip32_key_from_seed(
        seed,
        wally.BIP32_VER_MAIN_PRIVATE, 0)
    wallet_derived_key = wally.bip32_key_from_parent(
        wallet_master_key,
        1,
        wally.BIP32_FLAG_KEY_PRIVATE)
    address = wally.bip32_key_to_address(
        wallet_derived_key,
        wally.WALLY_ADDRESS_TYPE_P2PKH,
        wally.WALLY_ADDRESS_VERSION_P2PKH_LIQUID)
    # end-create_p2pkh_address
    print("")
    #print(F"Wallet Mster Key Derivation 1: {wallet_derived_key.to_wif()}")
    private_key = wally.bip32_key_to_base58(wallet_derived_key,wally.BIP32_FLAG_KEY_PRIVATE)
    print( "derived key : " + private_key)
    print( F"derived priv key (hexlified) {binascii.hexlify(wally.bip32_key_get_priv_key(wallet_derived_key))}")
    print(binascii.hexlify(wally.bip32_key_get_priv_key(wallet_derived_key)).decode())
    
    # start-derive_blinding_key
    master_blinding_key = wally.asset_blinding_key_from_seed(seed)
    script_pubkey = wally.address_to_scriptpubkey(
        address,
        wally.WALLY_NETWORK_LIQUID)
    private_blinding_key = wally.asset_blinding_key_to_ec_private_key(
        master_blinding_key,
        script_pubkey)
    public_blinding_key = wally.ec_public_key_from_private_key(
        private_blinding_key)
    # end-derive_blinding_key

    # start-create_conf_address
    confidential_address = wally.confidential_addr_from_addr(
        address,
        wally.WALLY_CA_PREFIX_LIQUID,
        public_blinding_key)
    # end-create_conf_address

    print("")
    print(F"Confidential Address: {confidential_address}")
    return private_key, confidential_address



# this method registers the given asset to the well-known entries of the node
def register_asset_id( asset_id ):
    
    privk = paramiko.Ed25519Key.from_private_key_file('/home/juergen/.ssh/id_ed25519')

    Client = paramiko.SSHClient()

    Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    Client.connect(hostname='lab.r3c.network',username='ubuntu', pkey=privk)

    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command('ls /var/www/html/.well-known/')
    response = ssh_stdout.readlines()

    ASSET_ID = '87fc8616ee664d005bdce9645b1c4e85971b3341010c4e9078cbfa8deb7424b6'
    ASSET_ID_STRING = "Authorize linking the domain name lab.r3c.network to the Liquid asset " + ASSET_ID

    #create_file = 'touch /var/www/html/.well-known/liquid-asset-proof-' + ASSET_ID
    print(F'touch /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command(F'touch /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    response = ssh_stdout.readlines()

    print(F'echo {ASSET_ID_STRING} | sudo tee -a /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    ssh_stdin, ssh_stdout, ssh_stderr = Client.exec_command(F'echo {ASSET_ID_STRING} | sudo tee -a /var/www/html/.well-known/liquid-asset-proof-{ASSET_ID}')
    response = ssh_stdout.readlines()


    Client.close()

    print(response)


def register_asset_id_on_liquid( asset_id ):
    ASSET_ID = '87fc8616ee664d005bdce9645b1c4e85971b3341010c4e9078cbfa8deb7424b6'
    CONTRACT = '{"entity":{"domain":"lab.r3c.network"}, "issuer_pubkey":"03eccefbf369c0300ef41102eed6d23c97cfbab143569f7c51031cbad260fe6dc9", "name":"Liquid SPAR", "precision":0, "ticker":"L-SPR", "version":0}'


    register_request = ['curl', 'https://assets.blockstream.info/', '-H', 'Content-Type: application/json', '-d', F'{{"asset_id":"{ASSET_ID}","contract":{CONTRACT}}}']


    # For registering the asset within Blockstream's asset registry
    register_response = subprocess.run(register_request, capture_output=True)


    if (register_response.returncode == 0):
        print(register_response.stdout.decode('ASCII'))
    else:
        print(register_response.returncode)