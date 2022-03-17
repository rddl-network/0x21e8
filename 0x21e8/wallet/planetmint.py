from planetmint_driver import Planetmint
from cryptoconditions.crypto import Ed25519SigningKey, Ed25519VerifyingKey

import binascii



def get_planetmint_keys():
    sk_raw=Ed25519SigningKey.generate_with_seed(binascii.unhexlify(b'2b4be7f19ee27bbf30c667b642d5f4aa69fd169872f8fc3059c08ebae2eb19e7'))
    my_vk = sk_raw.get_verifying_key().encode(encoding='base58')
    sk = sk_raw.encode(encoding='base58')
    return sk, my_vk
    
    