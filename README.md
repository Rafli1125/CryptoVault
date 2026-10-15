# CryptoVault — UTS Kriptografi

Aplikasi web lokal berbasis Python dan Flask untuk demonstrasi enkripsi/dekripsi delapan algoritma: Vigenère, Auto-Key Vigenère, Extended Vigenère, Playfair, Affine, Hill, Super Enkripsi, dan Enigma.

## Fitur

- Enkripsi dan dekripsi melalui antarmuka web.
- Input pesan teks untuk semua algoritma.
- Input file teks UTF-8 untuk algoritma alfabet.
- Input file teks maupun biner hingga 50 MB untuk Extended Vigenère dan Super Enkripsi.
- Hasil byte ditampilkan sebagai Base64 bila diperlukan dan tetap dapat diunduh sebagai berkas asli.
- Pengujian regresi fungsi algoritma melalui `unittest`.

## Persyaratan

- Python 3.10 atau lebih baru.
- `pip`.
- Browser modern.

## Menjalankan di Windows

Buka PowerShell pada folder project `CryptoVault`, lalu jalankan:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Jika PowerShell menolak aktivasi virtual environment, jalankan perintah berikut pada sesi PowerShell tersebut, lalu aktifkan ulang:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Buka alamat berikut di browser:

```text
http://127.0.0.1:5000
```

## Menjalankan di Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python app.py
```

## Kunci contoh di antarmuka

Kunci contoh yang ditampilkan pada form sengaja berbeda dari kunci yang digunakan pada contoh pengujian laporan.

| Algoritma | Kunci contoh | Format |
|---|---|---|
| Vigenère | `ORBIT` | Kata alfabet |
| Auto-Key Vigenère | `FALCON` | Kata alfabet |
| Extended Vigenère | `BYTEKEY` | Teks, dikonversi menjadi byte UTF-8 |
| Playfair | `SECURE` | Kata kunci; I/J digabung |
| Affine | `7,3` | Dua bilangan bulat `a,b`; `a` harus relatif prima dengan 26 |
| Hill | `3,2;5,7` | Matriks 2×2 atau 3×3 yang invertibel modulo 26 |
| Super Enkripsi | `CIPHER` | Digunakan untuk Extended Vigenère dan transposisi kolom |
| Enigma | `QWE` | Tiga huruf posisi awal rotor |

## Input teks, Base64, dan file

- Vigenère, Auto-Key Vigenère, Playfair, Affine, Hill, dan Enigma bekerja pada huruf ASCII A–Z. Angka, spasi, tanda baca, dan karakter non-ASCII diabaikan sesuai karakteristik cipher alfabet.
- File untuk cipher alfabet harus berupa teks UTF-8. File biner ditolak untuk mencegah data biner rusak ketika dibaca sebagai teks.
- Extended Vigenère dan Super Enkripsi bekerja pada byte, sehingga dapat digunakan untuk file teks maupun file biner. Maksimum ukuran unggahan adalah 50 MB.
- Pada mode **Pesan Teks**, ciphertext Extended Vigenère/Super Enkripsi ditampilkan dalam Base64. Untuk dekripsi teks, tempel ciphertext Base64. Bila memproses file, unduh hasil enkripsi (`.enc`) dan unggah berkas tersebut pada mode File saat dekripsi.
- Base64 hanya representasi data biner, bukan algoritma enkripsi.
- Playfair dapat menambahkan karakter `X` sebagai padding. Hill menambahkan `X` jika panjang teks tidak sesuai ukuran blok. Padding dapat muncul pada hasil dekripsi; ini adalah batasan umum penyandian berbasis blok/pasangan tanpa metadata panjang plaintext.

## Super Enkripsi

Super Enkripsi mengombinasikan Extended Vigenère dan Columnar Transposition. Dekripsi membalik urutannya. Pada mode Pesan Teks, ciphertext Base64 didekode menjadi byte sebelum kedua tahap dekripsi dilakukan. Pada mode File, byte ciphertext diproses langsung.

## File contoh

Folder `samples/` menyediakan contoh teks, byte, gambar PNG, database SQLite, audio WAV, dan video MP4. Gunakan Extended Vigenère atau Super Enkripsi untuk menguji setiap jenis file biner dan memastikan hasil dekripsi disimpan dengan nama/ekstensi yang sesuai.

## Pengujian algoritma

Dari folder project, jalankan:

```powershell
python -m unittest discover -s tests -v
```

Tes ini memeriksa round-trip algoritma inti, termasuk Super Enkripsi untuk input byte dengan berbagai panjang.

## Batasan keamanan

CryptoVault adalah aplikasi pembelajaran untuk demonstrasi cipher klasik, bukan perangkat untuk melindungi data sensitif atau penggunaan produksi. Jangan gunakan kunci atau file rahasia sebagai bahan demonstrasi.
