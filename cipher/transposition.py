
from .extended_vigenere import extended_encrypt, extended_decrypt

def columnar_encrypt(data, key):
    if not key:
        raise ValueError("Kunci transposisi tidak boleh kosong.")
    cols = len(key)
    order = sorted(range(cols), key=lambda i: (key[i], i))
    rows = (len(data) + cols - 1) // cols
    out = bytearray()
    for col in order:
        for r in range(rows):
            idx = r*cols + col
            if idx < len(data):
                out.append(data[idx])
    return bytes(out)

def columnar_decrypt(data, key):
    if not key:
        raise ValueError("Kunci transposisi tidak boleh kosong.")
    cols = len(key)
    n = len(data)
    rows = (n + cols - 1) // cols
    remainder = n % cols
    lengths = [rows if remainder == 0 or c < remainder else rows-1 for c in range(cols)]
    order = sorted(range(cols), key=lambda i: (key[i], i))
    columns = {}
    pos = 0
    for col in order:
        ln = lengths[col]
        columns[col] = data[pos:pos+ln]
        pos += ln
    out = bytearray()
    for r in range(rows):
        for c in range(cols):
            if r < len(columns[c]):
                out.append(columns[c][r])
    return bytes(out)

def super_encrypt(data, key):
    return columnar_encrypt(extended_encrypt(data, key), key)

def super_decrypt(data, key):
    return extended_decrypt(columnar_decrypt(data, key), key)
