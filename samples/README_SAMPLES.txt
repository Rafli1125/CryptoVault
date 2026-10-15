CryptoVault — File Contoh Pengujian

Gunakan file di folder ini terutama dengan algoritma berbasis byte:
- sample_text.txt          : teks UTF-8 dengan angka, tanda baca, dan karakter non-ASCII.
- sample_alpha.txt         : file teks berisi huruf A-Z; cocok untuk cipher alfabet.
- sample.bin               : data biner dengan semua nilai byte 0-255.
- sample_image.png         : gambar PNG kecil.
- sample_database.sqlite   : database SQLite dengan tabel sample_records.
- sample_audio.wav         : audio WAV PCM mono.
- sample_video.mp4         : video MP4 kecil dengan audio.

Extended Vigenere dan Super Enkripsi dapat menerima semua file di atas. Untuk uji file,
jalankan Enkripsi pada file, unduh hasil .enc, kemudian unggah .enc yang sama dalam mode
File dengan operasi Dekripsi. Simpan file hasil dekripsi dengan nama/ekstensi hasil yang
diberikan aplikasi, lalu bandingkan dengan file contoh asli.

Cipher alfabet (Vigenère, Auto-Key, Playfair, Affine, Hill, Enigma) menerima file teks UTF-8,
tetapi hanya memproses huruf A-Z. Angka, spasi, tanda baca, dan format asli tidak dipertahankan.
Jangan gunakan cipher alfabet untuk menguji file gambar, database, audio, video, atau biner.
