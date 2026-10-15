
def _validate_key(key):
    if not key:
        raise ValueError("Kunci Extended Vigenere tidak boleh kosong.")
    return bytes(key)

def extended_encrypt(data, key):
    key = _validate_key(key)
    return bytes((b + key[i % len(key)]) % 256 for i, b in enumerate(data))

def extended_decrypt(data, key):
    key = _validate_key(key)
    return bytes((b - key[i % len(key)]) % 256 for i, b in enumerate(data))
