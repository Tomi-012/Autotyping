# Analisis binary AutoTyping.exe

Tanggal analisis: 30 Oktober 2026. Metode: inspeksi statis dengan MCP REA, ekstraksi paket, pemeriksaan bytecode Python dengan REA, dan disassembly menggunakan Python 3.12. EXE tidak dijalankan selama analisis ini.

## Identitas dan cakupan

- File: `AutoTyping.exe`, 74.612.624 byte, PE32+ Windows x86-64.
- SHA-256: `D181942FBE5597C9EA300B5E407A34079503B6ABC64EC104F29A6C8808E520C1`.
- REA mengenali paket PyInstaller dengan Python 3.12 dan `python312.dll`. Metadata paket tidak menunjukkan penanda enkripsi. Ini tidak berarti seluruh data atau dependensi bebas proteksi.
- REA menginventarisasi 1.740 file yang teramati dalam grafik paket, termasuk isi PYZ; semua 1.740 hash yang tersedia berstatus verified dan tidak ada ketidakcocokan. Angka ini tidak sama dengan 1.057 entri CArchive di lapisan utama.
- File utama yang diekstrak adalah bytecode `AutoTyping`, yang mengidentifikasi nama sumber `AutoTyping.py`. SHA-256 hasil ekstraksi dengan header pyc yang direkonstruksi: `19d2819698a23370020ef736c81bdba65e6d3e3a1e854800407754df9f4211a4`. REA membaca 13 code object, termasuk module dan class, dengan cakupan parser lengkap untuk file tersebut.
- Hasil ekstraksi merupakan bytecode yang dipulihkan, bukan file sumber Python asli. Header `.pyc` direkonstruksi dari magic Python dalam paket; timestamp dan ukuran sumber pada header tersebut bukan bukti waktu pembuatan sumber.
- REA tidak menemukan direktori CLI .NET dalam PE luar. Tidak ada tabel sertifikat Authenticode tertanam pada PE; Windows `Get-AuthenticodeSignature` melaporkan `NotSigned` pada sistem ini. Penilaian rantai sertifikat atau kemungkinan tanda tangan katalog terpisah bukan cakupan parser REA.

## Susunan aplikasi

Program utama mengimpor `tkinter`, `scrolledtext`, `ttk`, `pyautogui`, `threading`, `time`, dan `keyboard`. Ia membuat root Tk, objek `AutoTypingApp`, lalu masuk ke `mainloop`. Folder paket juga memuat dependensi seperti Pillow, OpenCV dan NumPy; keberadaannya di paket saja tidak membuktikan dipakai langsung oleh kode utama maupun saat runtime.

Jendela berjudul **Auto Typing By Mas EJAAA**, ukuran awal 500 × 450 dan dapat diubah ukurannya. Status selalu di atas aktif pada awal program. Ada tab **Bot Typing** dan **Pengaturan**, area teks, tombol Mulai, Berhenti dan Bersihkan, pengaturan delay awal, pilihan metode dan label status.

| Pengaturan | Nilai awal | Rentang pada kontrol |
|---|---:|---:|
| Delay awal | 3 detik | 1–10 detik |
| Metode | batch | karakter, batch, keyboard |
| Delay per karakter | 0,001 detik | 0,0001–0,1 detik |
| Ukuran batch | 20 karakter | 5–50 karakter |
| Delay antar batch | 0,005 detik | 0,001–0,1 detik |
| Selalu di atas | aktif | dapat diubah lewat checkbox |

Rentang di atas adalah parameter kontrol Spinbox, bukan bukti bahwa setiap input manual divalidasi sebelum digunakan.

## Alur dan fungsi

1. `start_typing` membaca teks untuk mengecek apakah kosong setelah `strip()`. Jika kosong, status menampilkan pesan error. Bila ada teks, `is_typing` menjadi benar, tombol Mulai dinonaktifkan, tombol Berhenti diaktifkan, dan worker daemon `perform_typing` dibuat.
2. Worker membaca ulang teks dan delay dari widget, menampilkan hitungan mundur setiap satu detik, lalu membaca metode yang dipilih. Pengguna perlu memindahkan fokus ke tempat tujuan selama jeda. Program tidak menyimpan target jendela secara eksplisit.
3. `type_char_by_char` melakukan iterasi setiap karakter, memeriksa `is_typing`, memanggil `pyautogui.write(char)` dan tidur sesuai `typing_speed`.
4. `type_by_batch` mengubah teks menjadi daftar karakter, mengambil potongan dengan ukuran batch, memanggil `pyautogui.write(batch)` dan tidur sesuai `batch_delay`. Pembatalan diperiksa di antara batch, bukan di antara karakter di dalam satu panggilan batch.
5. `type_with_keyboard_api` melakukan iterasi setiap karakter, memeriksa `is_typing`, lalu memanggil `keyboard.write(char)`; pengaturan delay karakter dan batch tidak dipakai dalam jalur ini.
6. Jika flag masih benar saat worker selesai, program mengembalikan keadaan tombol dan menampilkan pesan selesai. `stop_typing` mengubah flag menjadi false, segera mengaktifkan tombol Mulai dan menampilkan status berhenti. `clear_text` menghapus isi editor dan memperbarui status.

Teks aktual dibaca menggunakan `Text.get('1.0', tk.END)` tanpa `strip()`; `strip()` hanya dipakai untuk pengecekan kosong. Widget Tk Text menyertakan newline terminal, sehingga alur ini berpotensi menambahkan Enter di akhir hasil ketik. Dampaknya bergantung pada perilaku library dan aplikasi tujuan; belum diuji langsung.

## Temuan teknis dan risiko

### 1. Delay karakter aktual lebih besar dari nilai UI

Bytecode PyAutoGUI yang dibundel mengatur `PAUSE = 0.1` dan membungkus `typewrite`/`write` dengan pemeriksaan fail-safe serta `_handlePause`, yang memanggil `sleep(PAUSE)` secara default setelah panggilan. Kode utama tidak mengubah `PAUSE` dan tidak memberikan `_pause=False`. Karena metode karakter memanggil `write` sekali untuk setiap karakter, ada tambahan sekitar 0,1 detik per panggilan selain delay yang dipilih, belum termasuk biaya lain. Ini menjelaskan mengapa nilai 0,001 detik bukan jaminan 1.000 karakter per detik. Metode batch membayar jeda default sekali per batch, sehingga bisa lebih cepat relatif terhadap metode karakter. Angka ini merupakan analisis statis, bukan pengukuran kecepatan aktual.

### 2. Berhenti dan mulai cepat berpotensi menyebabkan worker bertumpuk

Tombol Berhenti langsung mengaktifkan tombol Mulai tanpa menunggu worker sebelumnya selesai, sedangkan kedua worker berbagi flag boolean `is_typing`. Jika Mulai ditekan lagi sebelum worker lama memeriksa flag, flag kembali true dan worker lama dapat melanjutkan bersamaan dengan worker baru. Selama `sleep` atau satu panggilan `pyautogui.write(batch)`, pembatalan tidak langsung menghentikan panggilan tersebut. Ini adalah risiko yang mengikuti struktur kode; belum direproduksi secara live.

### 3. Pengecualian dapat meninggalkan UI dalam keadaan tidak siap

Worker tidak memperlihatkan blok `try/finally` untuk memulihkan tombol dan flag jika pembacaan pengaturan, library keyboard, atau pemanggilan PyAutoGUI gagal. PyAutoGUI yang dibundel memiliki fail-safe aktif; pemicunya dapat menghasilkan exception. Jika exception terjadi di worker, ada kemungkinan tombol tetap dalam keadaan sedang mengetik. Kondisi aktual dan pesan yang muncul belum diuji.

### 4. Akses Tkinter dari worker

`perform_typing` membaca widget dan variabel Tk serta mengubah label dan tombol dari thread worker. Ini dapat menimbulkan perilaku tidak konsisten atau error pada situasi tertentu, terutama saat jendela ditutup atau terjadi interaksi bersamaan. Pemeriksaan ini adalah tinjauan struktur statis, bukan bukti error pasti terjadi.

### 5. Ketepatan karakter dan fokus perlu diuji

Ketiga jalur mengirim input melalui library keyboard ke aplikasi yang sedang menerima fokus. Tidak ada validasi hasil di aplikasi tujuan pada kode utama. Perilaku karakter Unicode, baris baru, layout keyboard, aplikasi dengan hak akses berbeda, dan teks panjang perlu pengujian di target yang diinginkan. Nama metode dan label kecepatan bukan bukti kompatibilitas atau performa pada semua aplikasi.

### 6. Kontrol input dan penyimpanan

Tidak terlihat validasi eksplisit sebelum nilai spinbox dipakai untuk `range` atau `sleep`; nilai yang tidak valid berpotensi menimbulkan exception. Pada 13 code object utama, tidak ditemukan panggilan eksplisit untuk menyimpan pengaturan, membaca file teks, atau mengirim data melalui jaringan. Kesimpulan ini terbatas pada kode utama yang diperiksa; keberadaan modul jaringan dalam paket dan pemuatan dinamis berarti hal itu bukan audit menyeluruh terhadap seluruh dependensi atau perilaku runtime.

## Prioritas perbaikan yang disarankan

1. Gunakan objek pembatalan terpisah per worker, cegah worker baru sampai worker lama selesai, dan periksa pembatalan dengan interval yang sesuai.
2. Gunakan `try/finally` untuk selalu memulihkan status dan tombol, serta tampilkan kesalahan yang dapat dipahami pengguna.
3. Jalankan seluruh akses widget Tk pada main thread, misalnya menjadwalkan pembaruan melalui `root.after`.
4. Tentukan kebijakan newline terakhir, lakukan validasi nilai numerik, dan uji Unicode serta layout keyboard pada aplikasi tujuan.
5. Tentukan kecepatan yang diinginkan dengan mempertimbangkan `pyautogui.PAUSE`, lalu ukur hasil nyata dan respons tombol berhenti pada ketiga metode.

## Bukti dan batas

- `rea_evidence.json`: bundle bukti REA, termasuk identitas PE, import, sertifikat, inventaris paket, ekstraksi, dan parser bytecode. ID utama: `ev_2d1c3a100c67a7c51b65e388f44d61b0aec3b5a3eef61a49c12b0205f229a450` (inventaris), `ev_e38e73ef6a8b85fd2c4a9a5faea30f6f94e5eb240fcb71356fbb4a7e4299b3b7` (ekstraksi), `ev_e496050136738e95071953182352e481806b465dba1700872e22790bedac3a76` (kode utama).
- `AutoTyping.recovered.pyc`: salinan bytecode utama hasil ekstraksi REA, dengan header rekonstruksi.
- `disassembly.txt`: instruksi seluruh 13 code object utama; nomor baris berasal dari metadata bytecode, bukan sumber yang berhasil dipulihkan.
- `pyautogui_disassembly.txt`: disassembly dependensi PyAutoGUI yang dibundel, digunakan untuk memeriksa PAUSE dan pembungkus `write`.
- `disassemble.py`: skrip untuk membaca marshal dan menampilkan instruksi, tanpa memanggil atau menjalankan code object aplikasi. Ia tidak memulihkan komentar, format, atau sumber identik.

Tidak ada uji runtime, pemantauan jaringan, audit semua dependensi, pembuktian keamanan menyeluruh, atau pemulihan source code asli. Analisis statis dapat menunjukkan jalur dan potensi masalah, tetapi tidak membuktikan bahwa semua jalur terpanggil atau bahwa setiap risiko terjadi pada komputer pengguna.
