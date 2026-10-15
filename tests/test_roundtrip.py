"""Tes regresi mandiri untuk memastikan enkripsi/dekripsi algoritma konsisten.

Jalankan dari folder project dengan: python -m unittest discover -s tests -v
"""
import unittest
import base64

from cipher.vigenere import (
    vigenere_encrypt, vigenere_decrypt, autokey_encrypt, autokey_decrypt,
)
from cipher.extended_vigenere import extended_encrypt, extended_decrypt
from cipher.playfair import playfair_encrypt, playfair_decrypt, prepare
from cipher.affine import affine_encrypt, affine_decrypt
from cipher.hill import hill_encrypt, hill_decrypt
from cipher.transposition import super_encrypt, super_decrypt
from cipher.enigma import enigma_encrypt, enigma_decrypt


class CipherRoundTripTests(unittest.TestCase):
    def test_vigenere(self):
        plain, key = "NETWORKSECURITY", "ORBIT"
        self.assertEqual(vigenere_decrypt(vigenere_encrypt(plain, key), key), plain)

    def test_autokey_vigenere(self):
        plain, key = "NETWORKSECURITY", "FALCON"
        self.assertEqual(autokey_decrypt(autokey_encrypt(plain, key), key), plain)

    def test_extended_vigenere_all_byte_values(self):
        plain = bytes(range(256)) + b"\x00\xff\x10CryptoVault"
        key = "BYTEKEY".encode("utf-8")
        self.assertEqual(extended_decrypt(extended_encrypt(plain, key), key), plain)

    def test_playfair_with_documented_padding(self):
        plain, key = "NETWORK", "SECURE"
        ciphertext = playfair_encrypt(plain, key)
        # Playfair memasangkan huruf dan menambahkan X bila diperlukan. Hasil
        # dekripsi dibandingkan dengan teks yang memang telah disiapkan algoritma.
        self.assertEqual(playfair_decrypt(ciphertext, key), "".join(prepare(plain)))

    def test_affine(self):
        plain, a, b = "NETWORKSECURITY", 7, 3
        self.assertEqual(affine_decrypt(affine_encrypt(plain, a, b), a, b), plain)

    def test_hill_2x2(self):
        plain, key = "NETWORKS", "3,2;5,7"
        self.assertEqual(hill_decrypt(hill_encrypt(plain, key), key), plain)

    def test_hill_3x3(self):
        plain = "ACT"
        key = "6,24,1;13,16,10;20,17,15"
        self.assertEqual(hill_decrypt(hill_encrypt(plain, key), key), plain)

    def test_super_encryption_text_and_binary(self):
        key = b"CIPHER"
        payloads = [
            b"HELLOWORLD",
            bytes(range(256)),
            b"\x00\xff\x10" * 37,
            "Teks UTF-8: kriptografi, café, dan pesan.".encode("utf-8"),
        ]
        for payload in payloads:
            with self.subTest(size=len(payload)):
                self.assertEqual(super_decrypt(super_encrypt(payload, key), key), payload)

    def test_super_encryption_base64_text_round_trip(self):
        # Meniru alur UI: ciphertext byte ditampilkan sebagai Base64, lalu
        # Base64 didekode sebelum masuk ke fungsi dekripsi.
        plain, key = b"HELLOWORLD", b"CIPHER"
        cipher_b64 = base64.b64encode(super_encrypt(plain, key)).decode("ascii")
        decoded_cipher = base64.b64decode("".join(cipher_b64.split()), validate=True)
        self.assertEqual(super_decrypt(decoded_cipher, key), plain)

    def test_super_encryption_many_lengths(self):
        key = b"CIPHER"
        for length in range(0, 130):
            payload = bytes((i * 37) % 256 for i in range(length))
            with self.subTest(length=length):
                self.assertEqual(super_decrypt(super_encrypt(payload, key), key), payload)

    def test_super_encryption_repeated_and_short_keys(self):
        for key in (b"CIPHER", b"LETTER", b"A", b"LONGKEY", b"ZZZZ"):
            for length in range(0, 65):
                payload = bytes((i * 19 + length) % 256 for i in range(length))
                with self.subTest(key=key, length=length):
                    self.assertEqual(super_decrypt(super_encrypt(payload, key), key), payload)

    def test_enigma(self):
        plain, key = "HELLOWORLD", "QWE"
        self.assertEqual(enigma_decrypt(enigma_encrypt(plain, key), key), plain)


if __name__ == "__main__":
    unittest.main(verbosity=2)
