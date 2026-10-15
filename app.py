"""CryptoVault: aplikasi demonstrasi algoritma kriptografi klasik berbasis Flask."""

import base64
import binascii
import io
import os
from typing import Tuple

from flask import Flask, jsonify, render_template, request, send_file

from cipher.vigenere import (
    vigenere_encrypt,
    vigenere_decrypt,
    autokey_encrypt,
    autokey_decrypt,
)
from cipher.extended_vigenere import extended_encrypt, extended_decrypt
from cipher.playfair import playfair_encrypt, playfair_decrypt
from cipher.affine import affine_encrypt, affine_decrypt
from cipher.hill import hill_encrypt, hill_decrypt
from cipher.transposition import super_encrypt, super_decrypt
from cipher.enigma import enigma_encrypt, enigma_decrypt

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

CIPHERS = {
    "vigenere": "Vigenère Cipher",
    "autokey": "Auto-Key Vigenère",
    "extended": "Extended Vigenère",
    "playfair": "Playfair Cipher",
    "affine": "Affine Cipher",
    "hill": "Hill Cipher",
    "super": "Super Enkripsi",
    "enigma": "Enigma Cipher",
}
BYTE_CIPHERS = {"extended", "super"}


def clean_alpha(value: str) -> str:
    """Sesuai spesifikasi cipher alfabet: pertahankan huruf ASCII A-Z saja."""
    return "".join(ch for ch in value.upper() if ch.isascii() and ch.isalpha())


def key_to_bytes(key: str) -> bytes:
    key_bytes = key.strip().encode("utf-8")
    if not key_bytes:
        raise ValueError("Kunci wajib diisi.")
    return key_bytes


def output_filename(filename: str, action: str, is_file: bool) -> str:
    """Hasil enkripsi diberi .enc; saat dekripsi file *.enc, pulihkan nama asal."""
    name = os.path.basename(filename or "message.txt")
    if action == "decrypt" and is_file and name.lower().endswith(".enc"):
        name = name[:-4]
        return name or "decrypted_file"
    return name + (".enc" if action == "encrypt" else ".dec")


def is_displayable_text(data: bytes) -> Tuple[bool, str]:
    """True bila byte aman dibaca sebagai teks, bukan sekadar valid UTF-8."""
    try:
        value = data.decode("utf-8")
    except UnicodeDecodeError:
        return False, ""
    # Tab/newline/carriage return diperbolehkan; kontrol biner lain ditampilkan Base64.
    if any((ord(ch) < 32 and ch not in "\t\r\n") or ord(ch) == 127 for ch in value):
        return False, ""
    return True, value


@app.get("/")
def index():
    return render_template("index.html", ciphers=CIPHERS)


@app.post("/api/process")
def process():
    try:
        cipher_id = request.form.get("cipher", "vigenere").strip().lower()
        action = request.form.get("action", "encrypt").strip().lower()
        key = request.form.get("key", "")
        text = request.form.get("text", "")
        uploaded = request.files.get("file")
        is_file = bool(uploaded and uploaded.filename)

        if cipher_id not in CIPHERS:
            raise ValueError("Algoritma tidak dikenal. Pilih salah satu algoritma yang tersedia.")
        if action not in {"encrypt", "decrypt"}:
            raise ValueError("Operasi harus berupa enkripsi atau dekripsi.")
        if not key.strip():
            raise ValueError("Kunci wajib diisi.")

        filename = os.path.basename(uploaded.filename) if is_file else "message.txt"
        data = uploaded.read() if is_file else text.encode("utf-8")
        display_format = "text"

        # Cipher berbasis byte menerima sembarang data file. Pada mode teks, ciphertext
        # dimasukkan sebagai Base64 supaya byte biner dapat dipindahkan melalui textarea.
        if cipher_id in BYTE_CIPHERS:
            key_bytes = key_to_bytes(key)
            if not is_file and action == "decrypt":
                pasted = "".join(text.split())
                if not pasted:
                    raise ValueError(
                        "Untuk dekripsi Extended Vigenère/Super Enkripsi pada mode Pesan Teks, "
                        "tempelkan ciphertext dalam format Base64. Jika ciphertext berupa file, "
                        "pilih mode File."
                    )
                try:
                    data = base64.b64decode(pasted, validate=True)
                except (binascii.Error, ValueError, TypeError) as exc:
                    raise ValueError(
                        "Ciphertext tidak terbaca sebagai Base64. Salin hasil enkripsi lengkap, "
                        "atau gunakan file ciphertext pada mode File."
                    ) from exc

            if cipher_id == "extended":
                result_bytes = (
                    extended_encrypt(data, key_bytes)
                    if action == "encrypt"
                    else extended_decrypt(data, key_bytes)
                )
            else:
                result_bytes = (
                    super_encrypt(data, key_bytes)
                    if action == "encrypt"
                    else super_decrypt(data, key_bytes)
                )

            result_b64 = base64.b64encode(result_bytes).decode("ascii")
            # Mode file selalu menampilkan Base64 di area hasil; data hasil asli tetap
            # tersedia melalui tombol unduh. Untuk dekripsi teks, tampilkan teks asli bila layak.
            if is_file or action == "encrypt":
                display = result_b64
                display_format = "base64"
            else:
                readable, decoded_text = is_displayable_text(result_bytes)
                if readable:
                    display = decoded_text
                    display_format = "text"
                else:
                    display = result_b64
                    display_format = "base64"
            result_size = len(result_bytes)
        else:
            # Algoritma alfabet dapat memproses teks atau file teks UTF-8. File biner
            # ditolak dengan pesan jelas agar byte tidak rusak akibat decoding pengganti.
            try:
                source = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError(
                    "Algoritma ini bekerja pada huruf alfabet, bukan file biner. Gunakan file "
                    "teks UTF-8 atau pilih Extended Vigenère/Super Enkripsi untuk file biner."
                ) from exc

            if cipher_id == "vigenere":
                letters = clean_alpha(source)
                result_text = vigenere_encrypt(letters, key) if action == "encrypt" else vigenere_decrypt(letters, key)
            elif cipher_id == "autokey":
                letters = clean_alpha(source)
                result_text = autokey_encrypt(letters, key) if action == "encrypt" else autokey_decrypt(letters, key)
            elif cipher_id == "playfair":
                result_text = playfair_encrypt(source, key) if action == "encrypt" else playfair_decrypt(source, key)
            elif cipher_id == "affine":
                parts = [part.strip() for part in key.split(",")]
                if len(parts) != 2:
                    raise ValueError("Kunci Affine harus berbentuk a,b. Contoh format: 7,3")
                try:
                    a, b = int(parts[0]), int(parts[1])
                except ValueError as exc:
                    raise ValueError("Kunci Affine harus berupa dua bilangan bulat, misalnya 7,3.") from exc
                letters = clean_alpha(source)
                result_text = affine_encrypt(letters, a, b) if action == "encrypt" else affine_decrypt(letters, a, b)
            elif cipher_id == "hill":
                letters = clean_alpha(source)
                result_text = hill_encrypt(letters, key) if action == "encrypt" else hill_decrypt(letters, key)
            elif cipher_id == "enigma":
                letters = clean_alpha(source)
                result_text = enigma_encrypt(letters, key) if action == "encrypt" else enigma_decrypt(letters, key)
            else:  # Defensive fallback; all cipher IDs have been covered above.
                raise ValueError("Algoritma belum memiliki handler proses.")

            result_bytes = result_text.encode("utf-8")
            result_b64 = base64.b64encode(result_bytes).decode("ascii")
            display = result_text
            display_format = "text"
            result_size = len(result_bytes)

        return jsonify({
            "ok": True,
            "cipher": CIPHERS[cipher_id],
            "action": action,
            "display": display,
            "display_format": display_format,
            "base64": result_b64,
            "filename": output_filename(filename, action, is_file),
            "size": result_size,
            "is_file": is_file,
            "binary_cipher": cipher_id in BYTE_CIPHERS,
        })
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.post("/api/download")
def download():
    try:
        payload = request.get_json(silent=True) or {}
        encoded = payload.get("base64", "")
        if not encoded:
            raise ValueError("Tidak ada hasil untuk diunduh.")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError, TypeError) as exc:
            raise ValueError("Data unduhan tidak valid. Jalankan proses kembali.") from exc
        name = os.path.basename(payload.get("filename", "hasil.enc")) or "hasil.enc"
        return send_file(
            io.BytesIO(raw),
            as_attachment=True,
            download_name=name,
            mimetype="application/octet-stream",
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"ok": False, "error": "Ukuran file melebihi batas 50 MB."}), 413


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
