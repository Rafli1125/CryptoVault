const cipher = document.getElementById("cipher");
const key = document.getElementById("key");
const hint = document.getElementById("hint");
const keyLabel = document.getElementById("keyLabel");
const textMode = document.getElementById("textMode");
const fileMode = document.getElementById("fileMode");
const textPanel = document.getElementById("textPanel");
const filePanel = document.getElementById("filePanel");
const result = document.getElementById("result");
const statusEl = document.getElementById("status");
const inputHint = document.getElementById("inputHint");
const fileHint = document.getElementById("fileHint");
const resultNote = document.getElementById("resultNote");
const textInput = document.getElementById("text");
let lastBase64 = "";
let lastFilename = "hasil.enc";
let working = false;

// Petunjuk format input tetap ditampilkan, tetapi nilai kunci tidak diisi otomatis.
const hints = {
  vigenere: "Kunci berupa huruf alfabet ASCII.",
  autokey: "Kunci awal berupa huruf alfabet ASCII.",
  extended: "Kunci teks akan diubah menjadi byte UTF-8.",
  playfair: "I/J digabung dalam matriks Playfair 5×5.",
  affine: "Format parameter: a,b. Nilai a harus relatif prima dengan 26.",
  hill: "Gunakan matriks 2×2 atau 3×3 yang memiliki invers modulo 26.",
  super: "Kunci digunakan untuk Extended Vigenère dan urutan transposisi kolom.",
  enigma: "Masukkan tiga huruf untuk menentukan posisi awal rotor."
};
const byteCiphers = new Set(["extended", "super"]);

function currentCipherIsByte() {
  return byteCiphers.has(cipher.value);
}

function setStatus(label) {
  statusEl.innerHTML = `<i></i> ${label}`;
}

function updateInputHelp() {
  const byteCipher = currentCipherIsByte();
  if (inputHint) {
    inputHint.textContent = byteCipher
      ? "Enkripsi teks menerima plaintext biasa. Untuk dekripsi teks, tempel ciphertext dalam Base64. Jika memakai file, pilih kembali file ciphertext hasil unduhan."
      : "Hanya huruf ASCII A–Z yang diproses; angka, spasi, dan tanda baca diabaikan. File harus berupa teks UTF-8.";
  }
  if (fileHint) {
    fileHint.textContent = byteCipher
      ? "Mendukung file teks dan biner hingga 50 MB. Simpan hasil enkripsi melalui Download Hasil, lalu unggah file .enc tersebut untuk dekripsi."
      : "File harus berupa teks UTF-8. Sesuai karakteristik cipher alfabet, hanya huruf A–Z diproses sehingga format asli, spasi, angka, dan tanda baca tidak dipertahankan.";
  }
  if (textInput) {
    textInput.placeholder = byteCipher
      ? "Enkripsi: masukkan plaintext. Dekripsi: tempel ciphertext Base64..."
      : "Masukkan pesan yang akan dienkripsi atau didekripsi...";
  }
}

function updateCipher() {
  if (!cipher) return;
  const config = hints[cipher.value];
  if (!config) return;
  hint.textContent = config;
  // Selalu minta pengguna memasukkan kunci sendiri untuk algoritma yang dipilih.
  key.value = "";
  if (keyLabel) {
    if (cipher.value === "enigma") keyLabel.textContent = "POSISI AWAL ROTOR";
    else if (cipher.value === "affine") keyLabel.textContent = "PARAMETER KUNCI (a,b)";
    else if (cipher.value === "hill") keyLabel.textContent = "MATRIKS KUNCI";
    else keyLabel.textContent = "KUNCI";
  }
  updateInputHelp();
}

function showPage(page) {
  document.querySelectorAll(".page-view").forEach(view => view.classList.remove("active-page"));
  const target = document.getElementById("page-" + page);
  if (target) target.classList.add("active-page");
  document.querySelectorAll(".top-nav").forEach(button => {
    button.classList.toggle("active", button.dataset.page === page);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelectorAll(".top-nav").forEach(button => {
  button.addEventListener("click", () => showPage(button.dataset.page));
});
document.querySelectorAll("[data-goto]").forEach(button => {
  button.addEventListener("click", () => {
    if (button.dataset.cipher && cipher) {
      cipher.value = button.dataset.cipher;
      updateCipher();
    }
    showPage(button.dataset.goto);
  });
});

if (cipher) cipher.addEventListener("change", updateCipher);
if (textMode) {
  textMode.addEventListener("click", () => {
    textMode.classList.add("active");
    fileMode.classList.remove("active");
    textPanel.classList.remove("hidden");
    filePanel.classList.add("hidden");
    updateInputHelp();
  });
}
if (fileMode) {
  fileMode.addEventListener("click", () => {
    fileMode.classList.add("active");
    textMode.classList.remove("active");
    filePanel.classList.remove("hidden");
    textPanel.classList.add("hidden");
    updateInputHelp();
  });
}

async function process(action) {
  if (working) return;
  const fd = new FormData();
  fd.append("cipher", cipher.value);
  fd.append("action", action);
  fd.append("key", key.value);
  const usingFile = !filePanel.classList.contains("hidden");

  if (usingFile) {
    const selectedFile = document.getElementById("file").files[0];
    if (!selectedFile) {
      alert("Pilih file terlebih dahulu.");
      return;
    }
    fd.append("file", selectedFile);
  } else {
    fd.append("text", textInput.value);
  }

  working = true;
  document.getElementById("encrypt").disabled = true;
  document.getElementById("decrypt").disabled = true;
  setStatus("MEMPROSES");
  try {
    const response = await fetch("/api/process", { method: "POST", body: fd });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Pemrosesan gagal.");

    result.textContent = data.display;
    lastBase64 = data.base64;
    lastFilename = data.filename;
    document.getElementById("resultName").textContent = data.filename;
    document.getElementById("resultSize").textContent = `${data.size} byte`;
    document.getElementById("download").disabled = false;
    setStatus(action === "encrypt" ? "ENKRIPSI BERHASIL" : "DEKRIPSI BERHASIL");

    if (data.display_format === "base64") {
      resultNote.textContent = "Hasil ditampilkan sebagai Base64. Gunakan Download Hasil untuk menyimpan byte asli.";
    } else if (["playfair", "hill"].includes(cipher.value) && action === "decrypt") {
      resultNote.textContent = "Padding X dapat muncul pada hasil dekripsi Playfair/Hill sesuai aturan blok algoritma.";
    } else if (!currentCipherIsByte()) {
      resultNote.textContent = "Cipher alfabet mengabaikan spasi, angka, dan tanda baca; hasil hanya berisi huruf A–Z.";
    } else {
      resultNote.textContent = "Hasil teks berhasil dipulihkan. File hasil tetap dapat diunduh jika diperlukan.";
    }
  } catch (error) {
    setStatus("GAGAL");
    result.textContent = `Terjadi kesalahan: ${error.message}`;
    resultNote.textContent = "Periksa kunci, format input, dan mode teks/file kemudian coba lagi.";
    document.getElementById("download").disabled = true;
    lastBase64 = "";
    alert(error.message);
  } finally {
    working = false;
    document.getElementById("encrypt").disabled = false;
    document.getElementById("decrypt").disabled = false;
  }
}

if (document.getElementById("encrypt")) {
  document.getElementById("encrypt").addEventListener("click", () => process("encrypt"));
}
if (document.getElementById("decrypt")) {
  document.getElementById("decrypt").addEventListener("click", () => process("decrypt"));
}
if (document.getElementById("clear")) {
  document.getElementById("clear").addEventListener("click", () => {
    textInput.value = "";
    document.getElementById("file").value = "";
    result.textContent = "Hasil enkripsi atau dekripsi akan tampil di sini...";
    document.getElementById("resultName").textContent = "Belum ada hasil";
    document.getElementById("resultSize").textContent = "";
    lastBase64 = "";
    document.getElementById("download").disabled = true;
    setStatus("SIAP");
    resultNote.textContent = "Hasil dapat disalin atau diunduh sebagai file.";
  });
}
if (document.getElementById("copy")) {
  document.getElementById("copy").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(result.textContent);
      resultNote.textContent = "Hasil berhasil disalin ke clipboard.";
    } catch (_error) {
      alert("Clipboard tidak dapat diakses. Pilih dan salin hasil secara manual.");
    }
  });
}
if (document.getElementById("download")) {
  document.getElementById("download").addEventListener("click", async () => {
    if (!lastBase64) return;
    try {
      const response = await fetch("/api/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ base64: lastBase64, filename: lastFilename })
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Unduhan gagal.");
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = lastFilename;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
      resultNote.textContent = `File hasil disiapkan untuk diunduh: ${lastFilename}`;
    } catch (error) {
      alert(error.message);
    }
  });
}

updateCipher();
