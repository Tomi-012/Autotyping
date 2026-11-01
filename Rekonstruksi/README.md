# Auto Typing By Mas Rori

Jalankan `dist/AutoTyping-Mas-Rori.exe` pada Windows 64-bit. Aplikasi memakai ikon dari `Logo Mas Rori.ico` dan menyediakan dua tema. Saat pertama dibuka, tema oranye-hitam aktif; pilihan tema berikutnya disimpan secara lokal.

Pada tab **Template**, isi nama dan teks lalu pilih **Simpan**. Template yang tersimpan dapat dipilih pada tab **Bot Typing**, kemudian tombol **Tampilkan** akan mengganti isi kolom teks dengan template tersebut. Template dapat diubah atau dihapus dari tab Template. Data tersimpan di `%APPDATA%\AutoTyping Mas Rori\templates.json`, sedangkan pilihan tema di `theme.json` pada folder yang sama. Simpan cadangan file tersebut bila memindahkan komputer.

Kode pengetikan utama berasal dari bytecode yang diekstrak dengan MCP REA. `launcher.py`, `interface.py`, `templates.py`, dan `themes.py` adalah tambahan yang dapat dibaca, bukan source Python asli yang berhasil dipulihkan. Kelemahan logika pengetikan asli yang tercatat dalam `Analisis_REA/Laporan_Analisis.md` masih berlaku.

Pemeriksaan otomatis mencakup tampilan kontrol pada beberapa ukuran jendela di kedua tema, penyimpanan dan pembacaan template, serta ketiga jalur pengetikan dengan penerima tiruan. Pengiriman tombol ke aplikasi tujuan nyata belum diuji pada versi ini.

Untuk membangun ulang dengan Python 3.12:

```powershell
python -m pip install -r requirements-lock.txt
python -m PyInstaller --noconfirm --onefile --windowed --name AutoTyping-Mas-Rori --icon "Logo Mas Rori.ico" --add-data "AutoTyping.recovered.pyc;." --add-data "Logo Mas Rori.ico;." launcher.py
```

