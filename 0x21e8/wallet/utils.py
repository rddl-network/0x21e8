from mnemonic import Mnemonic


def create_and_save_seed(strength: int ) -> bytes:
    mnemonic_obj = Mnemonic("english")
    phrase = mnemonic_obj.generate(strength)
    seed_bytes = mnemonic_obj.to_seed(phrase, '0x21e8')
    with open("secret.txt", 'w') as secret:
        secret.write(seed_bytes.hex())
    return phrase

def get_seed_from_mnemonic(mnemonic: str) -> bytes:
    mnemonic_obj = Mnemonic("english")
    seed_bytes = mnemonic_obj.to_seed(mnemonic, '0x21e8')
    return seed_bytes


def save_seed_from_mnemonic(mnemonic: str):
    mnemonic_obj = Mnemonic("english")
    seed_bytes = mnemonic_obj.to_seed(mnemonic, '0x21e8')
    with open("secret.txt", 'w') as secret:
        secret.write(seed_bytes.hex())
