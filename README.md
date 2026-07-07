## Deskripsi Proyek

[cite_start]Proyek **"Peace Blur"** adalah aplikasi *Computer Vision* sederhana yang dibuat menggunakan Python[cite: 4, 24]. [cite_start]Aplikasi ini memanfaatkan **OpenCV** untuk memproses input video dari *webcam* dan memberikan efek *blur* [cite: 9, 25, 73][cite_start], serta **MediaPipe Tasks API** untuk melacak 21 titik koordinat pada jari tangan secara *real-time*[cite: 12, 26, 272]. 

[cite_start]Ketika kamera mendeteksi telapak tangan Anda membentuk simbol **Peace (✌️)**, seluruh tampilan layar kamera akan otomatis berubah menjadi buram total[cite: 21, 234, 272].

---

## Prasyarat Sistem & Catatan Penting ⚠️

> [cite_start]📌 **PENTING: Wajib Menggunakan Python 3.12 (Versi Stabil)** [cite: 153, 173]

[cite_start]Untuk menjalankan program ini dengan normal, Anda **harus mengunduh dan menggunakan Python versi 3.12**[cite: 153, 173]. 

**Mengapa harus Python 3.12?**
* [cite_start]**Kestabilan MediaPipe:** Framework AI dari Google (MediaPipe) memerlukan lingkungan Python versi stabil agar semua modul pelacakan tangan (`tasks/vision`) dapat terbaca dan bekerja dengan mulus[cite: 10, 271, 288, 303].
* [cite_start]**Menghindari Error Versi Baru:** Jika Anda mencoba menjalankan proyek ini menggunakan Python versi eksperimental yang terlalu baru (seperti Python 3.13 atau 3.14), program akan mengalami *crash* (*broken import*)[cite: 151, 152, 172]. [cite_start]Hal ini terjadi karena struktur internal MediaPipe belum diperbarui untuk mendukung versi Python tersebut[cite: 152, 331].

[cite_start]Oleh karena itu, sangat disarankan untuk membuat **Virtual Environment (`venv`)** berbasis Python 3.12 sebelum menginstal *dependencies* proyek ini[cite: 157, 266, 333].
