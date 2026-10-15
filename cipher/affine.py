
import math

def validate(a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError("Nilai a harus relatif prima dengan 26. Contoh valid: 1,3,5,7,9,11,15,17,19,21,23,25.")
    return a % 26, b % 26

def affine_encrypt(text, a, b):
    a, b = validate(a, b)
    return "".join(chr((a*(ord(c)-65)+b)%26+65)
                   for c in text.upper() if c.isalpha() and c.isascii())

def affine_decrypt(text, a, b):
    a, b = validate(a, b)
    inv = pow(a, -1, 26)
    return "".join(chr((inv*((ord(c)-65)-b))%26+65)
                   for c in text.upper() if c.isalpha() and c.isascii())
