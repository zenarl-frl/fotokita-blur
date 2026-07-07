## Deskripsi Proyek

Proyek **"Peace Blur"** adalah aplikasi *Computer Vision* sederhana yang dibuat menggunakan Python. Aplikasi ini memanfaatkan **OpenCV** untuk memproses input video dari *webcam* dan memberikan efek *blur* , serta **MediaPipe Tasks API** untuk melacak 21 titik koordinat pada jari tangan secara *real-time*
Ketika kamera mendeteksi telapak tangan Anda membentuk simbol **Peace (✌️)**, seluruh tampilan layar kamera akan otomatis berubah menjadi buram total.

---

## Prasyarat Sistem & Catatan Penting ⚠️

> 📌 **PENTING: Wajib Menggunakan Python 3.12 (Versi Stabil)**

Untuk menjalankan program ini dengan normal, Anda **harus mengunduh dan menggunakan Python versi 3.12**. 

**Mengapa harus Python 3.12?**
* **Kestabilan MediaPipe:** Framework AI dari Google (MediaPipe) memerlukan lingkungan Python versi stabil agar semua modul pelacakan tangan dapat terbaca dan bekerja dengan mulus.
* **Menghindari Error Versi Baru:** Jika Anda mencoba menjalankan proyek ini menggunakan Python versi eksperimental yang terlalu baru (seperti Python 3.13 atau 3.14), program akan mengalami *crash* (*broken import*). Hal ini terjadi karena struktur internal MediaPipe belum diperbarui untuk mendukung versi Python tersebut.

[cite_start]Oleh karena itu, sangat disarankan untuk membuat **Virtual Environment (`venv`)** berbasis Python 3.12 sebelum menginstal *dependencies* proyek ini.
