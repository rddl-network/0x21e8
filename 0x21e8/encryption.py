import ast
import nacl.secret
import nacl.utils
from sha3 import sha3_256

def get_secret_box():
    with open("secret.txt", "r") as secret:
        seed = bytes.fromhex(secret.readline())
    key = sha3_256( seed ).digest()
    box = nacl.secret.SecretBox(key)
    return box

def encrypt_dict( data: dict ):
    data_str = str(data).encode('utf-8')
    encrypted = encrypt_bytes(data_str)
    return encrypted

def encrypt_str( data: str ):
    encrypted = encrypt_bytes(data.encode('utf-8'))
    return encrypted

def encrypt_bytes( data: bytes ):
    box = get_secret_box()
    encrypted = box.encrypt(data)
    return encrypted

def decrypt_2_bytes( encrypted_data ):
    box = get_secret_box()
    return box.decrypt(encrypted_data)

def decrypt_2_str( encrypted_data ):
    decrypted_bytes = decrypt_2_bytes( encrypted_data )
    return decrypted_bytes.decode('utf-8')

def decrypt_2_dict( encrypted_data ):
    decrypted_str = decrypt_2_str(encrypted_data )
    decrytped_dict = ast.literal_eval( decrypted_str )
    return decrytped_dict
    
    
