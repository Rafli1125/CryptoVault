
import math

def parse_key(key):
    rows = []
    for row in key.strip().split(";"):
        vals = [int(x.strip()) for x in row.split(",") if x.strip()]
        if vals:
            rows.append(vals)
    if not rows or any(len(r) != len(rows) for r in rows):
        raise ValueError("Kunci Hill harus matriks persegi. Contoh 2x2: 3,3;2,5")
    n = len(rows)
    if n not in (2,3):
        raise ValueError("Versi ini mendukung matriks Hill 2x2 atau 3x3.")
    return [[x % 26 for x in r] for r in rows]

def det2(m): return (m[0][0]*m[1][1]-m[0][1]*m[1][0]) % 26

def det3(m):
    return (
        m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
        -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
        +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
    ) % 26

def inverse_matrix(m):
    n = len(m)
    d = det2(m) if n == 2 else det3(m)
    if math.gcd(d, 26) != 1:
        raise ValueError("Determinan matriks tidak memiliki inverse modulo 26.")

    invd = pow(d, -1, 26)
    if n == 2:
        return [
            [(invd*m[1][1])%26, (-invd*m[0][1])%26],
            [(-invd*m[1][0])%26, (invd*m[0][0])%26]
        ]

    cof = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            sub = [row[:j]+row[j+1:] for k,row in enumerate(m) if k != i]
            cof[i][j] = ((-1)**(i+j)) * (sub[0][0]*sub[1][1]-sub[0][1]*sub[1][0])
    adj = [[cof[j][i] for j in range(3)] for i in range(3)]
    return [[(invd*adj[i][j])%26 for j in range(3)] for i in range(3)]

def multiply(m, v):
    return [sum(m[i][j]*v[j] for j in range(len(v))) % 26 for i in range(len(m))]

def process(text, key, decrypt=False):
    m = parse_key(key)
    if decrypt:
        m = inverse_matrix(m)
    s = "".join(c for c in text.upper() if c.isalpha() and c.isascii())
    n = len(m)
    pad = (-len(s)) % n
    s += "X" * pad
    out = []
    for i in range(0, len(s), n):
        v = [ord(c)-65 for c in s[i:i+n]]
        out.extend(multiply(m, v))
    return "".join(chr(x+65) for x in out)

def hill_encrypt(text, key): return process(text, key, False)
def hill_decrypt(text, key): return process(text, key, True)
