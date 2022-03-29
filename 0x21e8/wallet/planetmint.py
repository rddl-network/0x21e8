from cryptoconditions.crypto import Ed25519SigningKey
from mnemonic import Mnemonic
from wallet.keymanagement import seed_to_extended_key
import binascii



def get_planetmint_keys( mnemonic_phrase ):
    seed = Mnemonic.to_seed( mnemonic_phrase, '0x21e8' )
    ext_seed = seed_to_extended_key(seed)
    sk_raw = Ed25519SigningKey.generate_with_seed(ext_seed.privkey)
    vk = sk_raw.get_verifying_key().encode(encoding='base58')
    sk = sk_raw.encode(encoding='base58')
    return sk, vk
    
    
#Planetmint raw private key: 8249232f45b8231e6765a9c2c180aac69c54a261fd618c97f84e464af871f -> done!
#Planetmint address private key: k4DYEbRbYBbehV2Qnq9vRD75PCWTkUTR
#Planetmint chaincode: 7fb5fb5fd8d7da70f62e33a3d592a4885bff857e3b23379a22c98bb8b9e2a0
#Planetmint address key: 2gs2o1dKRSFnPztDGPHHkWqwqixUCqjdT1vrZt
#Planetmint raw public key: 114715fbcea4e14ed6d24296ea6e11333372b8f12cb5bffdd21f3a327b2b24e
#Planetmint private key: bprv35Rc2dqCQhrCE9zjscZvJFeBfD93jbJLwDqgyPPwUHWC83neHVh4wfxceHyFu2WLHTdGhDpsKF9JXbRoS2TFYjcsZsN9pwRo9a3Bsk6A5CK
#Planetmint public key: bpubq8d4saQC76AjUXo9hNtSu1sCKD4CgGpXYvpNgZbgCEdekyfXLA3MHe5QSgeUU5WzYa5pTHWv2GMZzDpWF9FAM7ZBBUGuSpD4R9dFZMcFXvH
#MNEMONIC_PHRASE = 'supreme layer police brand month october rather rack proud strike receive joy limit random hill inside brand depend giant success quarter brain butter mechanic'
#get_planetmint_keys( MNEMONIC_PHRASE)