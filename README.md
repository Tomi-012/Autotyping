<div align="center">

# Auto Typing by Mas Rori

**Tulis sekali, gunakan kembali kapan saja.**

Aplikasi desktop Windows untuk mengetik teks secara otomatis dan menyimpan template yang sering digunakan.

![Windows](https://img.shields.io/badge/Windows-64--bit-0078D6?style=flat-square&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Interface](https://img.shields.io/badge/Antarmuka-Tkinter-FF7624?style=flat-square)
![Build](https://img.shields.io/badge/Build-PyInstaller-444444?style=flat-square)

[Mulai menggunakan](#mulai-menggunakan) · [Template](#menggunakan-template) · [Build dari proyek](#build-dari-proyek) · [Struktur proyek](#struktur-proyek)

</div>

---

## Tentang aplikasi

Auto Typing membantu memasukkan teks ke aplikasi yang sedang aktif. Tulis teks di kolom **Bot Typing**, tentukan jeda awal, lalu pindahkan kursor ke tempat tujuan sebelum hitungan mundur selesai.

Teks yang sering dipakai dapat disimpan sebagai template dan ditampilkan kembali kapan saja. Aplikasi menyediakan tema oranye-hitam dan tema default yang dapat diganti melalui menu **Pengaturan**.

## Fitur

- **Pengetikan otomatis** dengan tiga metode: karakter, batch, dan Keyboard API.
- **Jeda awal** untuk memberi waktu memindahkan kursor ke aplikasi tujuan.
- **Pengaturan kecepatan**, termasuk delay per karakter, ukuran batch, dan delay antar-batch.
- **Template lokal** untuk membuat, menyimpan, mengubah, menghapus, dan menggunakan kembali teks.
- **Dua tema**: oranye-hitam dan default. Pilihan terakhir disimpan untuk penggunaan berikutnya.
- **Selalu di atas** agar jendela aplikasi mudah dijangkau saat berpindah ke aplikasi lain.
- Tombol untuk **memulai**, **menghentikan**, dan **membersihkan** teks.

## Mulai menggunakan

### Persyaratan

- Windows 64-bit.
- File aplikasi [AutoTyping-Mas-Rori.exe](Rekonstruksi/dist/AutoTyping-Mas-Rori.exe).

Python tidak perlu dipasang untuk menjalankan file EXE yang sudah dibangun. Untuk mengubah kode atau membangun EXE sendiri, ikuti bagian [Build dari proyek](#build-dari-proyek).

### Mengetik teks

1. Buka `AutoTyping-Mas-Rori.exe`.
2. Masukkan teks pada tab **Bot Typing**.
3. Atur waktu pada **Mulai setelah** dan pilih metode di tab **Pengaturan** bila diperlukan.
4. Klik **Mulai Mengetik**, lalu pindahkan kursor ke kolom tujuan sebelum hitungan mundur selesai.
5. Gunakan tombol **Berhenti** jika ingin menghentikan pengetikan.

> Pastikan kolom tujuan sudah aktif sebelum hitungan mundur selesai. Aplikasi mengirimkan input ke jendela yang menerima fokus.

### Menggunakan template

1. Buka tab **Template**.
2. Isi nama dan teks, lalu klik **Simpan**.
3. Kembali ke tab **Bot Typing**, pilih template dari daftar, lalu klik **Tampilkan**.
4. Periksa teks dan klik **Mulai Mengetik** saat siap.

Tombol **Tampilkan** mengganti isi kolom Bot Typing dengan teks template. Untuk memperbarui template, pilih namanya di tab **Template**, ubah isinya, lalu klik **Simpan**. Tombol **Hapus** tersedia untuk menghapus template yang dipilih.

## Metode pengetikan

| Metode | Cara kerja | Pengaturan terkait |
| --- | --- | --- |
| **Karakter** | Mengirim teks satu karakter per panggilan melalui PyAutoGUI. | Delay per karakter. |
| **Batch** | Mengirim teks dalam beberapa kelompok karakter melalui PyAutoGUI. | Ukuran batch dan delay antar-batch. |
| **Keyboard API** | Mengirim teks satu karakter per panggilan melalui library `keyboard`. | Tidak menggunakan delay karakter atau batch. |

Kecepatan dan hasil pengetikan dapat berbeda bergantung pada metode dan aplikasi tujuan. Uji teks pendek terlebih dahulu, terutama saat menggunakan karakter khusus atau aplikasi yang sensitif terhadap kecepatan input.

## Penyimpanan data

Template dan pilihan tema disimpan secara lokal pada folder:

```text
%APPDATA%\AutoTyping Mas Rori\
├── templates.json   # Nama dan isi template
└── theme.json       # Pilihan tema
```

Isi template tersimpan sebagai teks dalam file JSON. Simpan cadangan `templates.json` jika ingin memindahkan template ke komputer lain. File ini dapat berisi informasi pribadi sesuai teks yang Anda simpan.

## Build dari proyek

Build berikut menggunakan **Python 3.12** pada Windows. Jalankan perintah dari root proyek melalui PowerShell:

```powershell
cd Rekonstruksi

# Buat lingkungan Python dan pasang dependensi.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt

# Bangun satu file EXE dengan ikon aplikasi.
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --windowed `
  --name AutoTyping-Mas-Rori `
  --icon "Logo Mas Rori.ico" `
  --add-data "AutoTyping.recovered.pyc;." `
  --add-data "Logo Mas Rori.ico;." `
  launcher.py
```

Hasil build berada di `Rekonstruksi\dist\AutoTyping-Mas-Rori.exe`.

### Tentang kode pengetikan

Mesin pengetikan menggunakan bytecode Python 3.12 yang diekstrak dari aplikasi sebelumnya melalui MCP REA. File `AutoTyping.recovered.pyc` diperlukan saat build dan runtime. Source Python asli untuk mesin tersebut tidak tersedia; file antarmuka, template, dan tema di folder `Rekonstruksi` merupakan kode proyek yang dapat dibaca dan diubah.

Laporan pemeriksaan dan batas analisis tersedia di [Analisis_REA/Laporan_Analisis.md](Analisis_REA/Laporan_Analisis.md).

## Struktur proyek

```text
.
├── README.md
├── Analisis_REA/                  # Laporan, disassembly, dan bukti analisis
└── Rekonstruksi/
    ├── dist/
    │   ├── AutoTyping-Mas-Rori.exe
    │   └── AutoTyping-Rekonstruksi.exe  # Versi rekonstruksi sebelumnya
    ├── AutoTyping.recovered.pyc   # Bytecode mesin pengetikan
    ├── interface.py               # Antarmuka utama dan pengaturan
    ├── launcher.py                # Titik masuk aplikasi
    ├── templates.py               # Pengelolaan template
    ├── themes.py                  # Tema dan preferensi tampilan
    ├── Logo Mas Rori.ico          # Ikon aplikasi
    ├── requirements-lock.txt      # Dependensi build
    └── README.md                  # Catatan build dan penggunaan
```

## Catatan penggunaan

- Pengetikan otomatis bergantung pada fokus dan perilaku aplikasi tujuan. Hasil pada setiap aplikasi dan layout keyboard belum tentu sama.
- Pengujian sebelumnya mencakup layout, pengelolaan template, dan jalur pengetikan dengan penerima tiruan. Pengiriman tombol langsung ke berbagai aplikasi tujuan belum diuji secara menyeluruh.
- Logika pengetikan dari aplikasi sebelumnya masih memiliki keterbatasan yang dijelaskan dalam laporan REA, termasuk kemungkinan proses bertumpuk jika pengetikan segera dimulai ulang setelah dihentikan.
