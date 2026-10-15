
def _validate_key(key):
    key = "".join(c for c in key.upper() if c.isalpha() and c.isascii())
    if not key:
        raise ValueError("Kunci harus mengandung minimal satu huruf alfabet.")
    return key

def vigenere_encrypt(text, key):
    key = _validate_key(key)
    text = "".join(c for c in text.upper() if c.isalpha() and c.isascii())
    return "".join(chr((ord(p)-65 + ord(key[i % len(key)])-65) % 26 + 65)
                   for i, p in enumerate(text))

def vigenere_decrypt(text, key):
    key = _validate_key(key)
    text = "".join(c for c in text.upper() if c.isalpha() and c.isascii())
    return "".join(chr((ord(c)-65 - (ord(key[i % len(key)])-65)) % 26 + 65)
                   for i, c in enumerate(text))

def autokey_encrypt(text, key):
    key = _validate_key(key)
    text = "".join(c for c in text.upper() if c.isalpha() and c.isascii())
    stream = key + text
    out = []
    for i, p in enumerate(text):
        k = ord(stream[i]) - 65
        out.append(chr(((ord(p)-65) + k) % 26 + 65))
    return "".join(out)

def autokey_decrypt(text, key):
    key = _validate_key(key)
    text = "".join(c for c in text.upper() if c.isalpha() and c.isascii())
    plain = []
    for i, c in enumerate(text):
        kchar = key[i] if i < len(key) else plain[i-len(key)]
        k = ord(kchar) - 65
        plain.append(chr(((ord(c)-65) - k) % 26 + 65))
    return "".join(plain)
