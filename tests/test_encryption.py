import sha3
import nacl.secret
from x21e8.wallet.seed import create_and_save_seed
from x21e8.encryption import encrypt_str, encrypt_dict, encrypt_bytes, decrypt_2_str, decrypt_2_dict, decrypt_2_bytes

try:
    secret = open("secret.txt", "r")
    seed = bytes.fromhex(secret.readline())
    assert nacl.secret.SecretBox.KEY_SIZE == sha3.sha3_256(seed).digest_size
except FileNotFoundError:
    create_and_save_seed(128)


def test_encryption_decryption_bytes():
    data = "teststring".encode()
    encrypted_data = encrypt_bytes(data)
    decrypted_data = decrypt_2_bytes(encrypted_data)
    assert data == decrypted_data


def test_encryption_decryption_str():
    data = "teststring"
    encrypted_data = encrypt_str(data)
    decrypted_data = decrypt_2_str(encrypted_data)
    assert data == decrypted_data


def test_encryption_decryption_dict():
    data = {"test": "test"}
    encrypted_data = encrypt_dict(data)
    decrypted_data = decrypt_2_dict(encrypted_data)
    assert data == decrypted_data
