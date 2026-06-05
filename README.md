# Grafika Start Menu

Aplikasi simulasi **Start Menu Windows** untuk Final Project Grafika Komputer.
Seluruh antarmuka dibuat manual menggunakan Python `ctypes`, Windows API, dan
GDI tanpa library GUI eksternal.

## Fitur

- Window native Windows melalui WinAPI
- Desktop dan taskbar bergaya modern
- Tombol START untuk membuka dan menutup menu
- Efek hover pada tombol dan item menu
- Menu Calculator, Notes, Settings, About, dan Exit
- Dialog native Windows untuk setiap fitur
- Gambar kotak, warna, dan teks secara manual dengan GDI
- Definisi tipe dan callback yang kompatibel dengan Windows 64-bit

## Persyaratan

- Windows 10 atau Windows 11
- Python 3 versi 64-bit
- Tidak memerlukan instalasi package tambahan

## Menjalankan

Clone repository, masuk ke direktori proyek, lalu jalankan:

```powershell
python main.py
```

## Teknologi

Program hanya menggunakan Python standard library:

- `ctypes`
- `ctypes.wintypes`
- `user32.dll`
- `gdi32.dll`
- `kernel32.dll`

Komponen antarmuka digambar menggunakan fungsi GDI seperti
`CreateSolidBrush`, `Rectangle`, `TextOutW`, `SetTextColor`, dan `SetBkMode`.
Event mouse dan proses menggambar ditangani melalui Windows message loop.

## Struktur Proyek

```text
Grafika-Final-Project/
|-- main.py
|-- README.md
|-- LICENSE
|-- .gitignore
`-- .gitattributes
```

## Batasan

Aplikasi ini khusus Windows karena memanggil WinAPI secara langsung. Program
tidak menggunakan Tkinter, PyQt, wxPython, Pygame, Kivy, atau library GUI siap
pakai lainnya.

## Lisensi

Proyek ini tersedia di bawah [MIT License](LICENSE).
