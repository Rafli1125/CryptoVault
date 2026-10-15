
import string

def make_matrix(key):
    raw = "".join(c for c in key.upper() if c.isalpha() and c.isascii()).replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    seq = []
    for c in raw + alphabet:
        if c not in seq:
            seq.append(c)
    return [seq[i:i+5] for i in range(0, 25, 5)]

def prepare(text):
    s = "".join(c for c in text.upper() if c.isalpha() and c.isascii()).replace("J", "I")
    pairs, i = [], 0
    while i < len(s):
        a = s[i]
        if i+1 >= len(s):
            b = "X"
            i += 1
        elif s[i] == s[i+1]:
            b = "X"
            i += 1
        else:
            b = s[i+1]
            i += 2
        pairs.append(a+b)
    return pairs

def transform_pair(a, b, matrix, encrypt=True):
    pos = {matrix[r][c]:(r,c) for r in range(5) for c in range(5)}
    ra, ca = pos[a]
    rb, cb = pos[b]
    step = 1 if encrypt else -1
    if ra == rb:
        return matrix[ra][(ca+step)%5] + matrix[rb][(cb+step)%5]
    if ca == cb:
        return matrix[(ra+step)%5][ca] + matrix[(rb+step)%5][cb]
    return matrix[ra][cb] + matrix[rb][ca]

def playfair_encrypt(text, key):
    matrix = make_matrix(key)
    return "".join(transform_pair(p[0], p[1], matrix, True) for p in prepare(text))

def playfair_decrypt(text, key):
    matrix = make_matrix(key)
    s = "".join(c for c in text.upper() if c.isalpha() and c.isascii()).replace("J","I")
    if len(s) % 2:
        raise ValueError("Ciphertext Playfair harus berjumlah genap.")
    return "".join(transform_pair(s[i], s[i+1], matrix, False) for i in range(0,len(s),2))
