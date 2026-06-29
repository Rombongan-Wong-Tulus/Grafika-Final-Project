# 👥 Pembagian Jobdesk Kelompok — Grafika Final Project

> Referensi pembagian tugas berdasarkan komponen `main.py` untuk 4 anggota kelompok.

---

## Ringkasan Pembagian

| Anggota | Jobdesk | Komponen di `main.py` |
|---------|---------|----------------------|
| **Akbar** | Popup & Dialog | Background, tile ikon desktop, dialog input file |
| **Dicky** | System Tray | System tray icon, hover effect |
| **Figa** | Event Interaction | Event handling, custom dialog info, message loop |
| **Rico** | Start Menu & Skeleton Graphics | Panel start menu, item-item menu, `run_menu_action` |

---

## Detail Per Anggota

---

### 💬 Akbar — Popup & Dialog

**Tanggung jawab:** Tampilan area desktop, tile ikon, dan seluruh sistem dialog (input file & dialog info/popup).

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Komponen | Deskripsi |
|-----------------|----------|-----------|
| Warna desktop | `BACKGROUND`, `ICON_BLUE`, `TEXT_PRIMARY`, `TEXT_SECONDARY` | Palet warna desktop |
| `draw_ui()` — bagian desktop | Blok background + tile ikon | Gambar desktop, judul, dan 3 tile ikon (PROJECT, FILES, SYSTEM) |
| `get_input_dialog_layout()` | Fungsi layout | Hitung posisi dialog input file di tengah layar |
| `draw_input_dialog()` | Fungsi render | Gambar dialog: header biru, input field dengan kursor `_`, tombol OK & Cancel |
| `open_file_dialog()` | Fungsi helper | Buka dialog input file (set state + `InvalidateRect`) |
| `get_msg_dialog_layout()` | Fungsi layout | Hitung posisi popup info secara dinamis sesuai jumlah baris teks |
| `draw_msg_dialog()` | Fungsi render | Gambar popup info: overlay gelap, header, ikon, konten multi-baris, tombol OK |
| `show_message()` | Fungsi helper | Set state popup info + trigger gambar ulang |
| State: `dialog_open`, `dialog_input`, `msg_dialog_open`, `msg_dialog_title`, `msg_dialog_lines` | State global | Kontrol buka/tutup semua dialog dan kontennya |

**Konsep yang perlu dipahami:**
- Cara kerja `draw_rect` dan `draw_text` (GDI primitives)
- Format COLORREF Windows (`rgb()` function)
- Simulasi kursor teks dengan karakter `"_"` di akhir string input
- Fungsi tidak langsung menggambar — hanya ubah state lalu panggil `InvalidateRect`, yang memicu `WM_PAINT`

---

### 🔷 Dicky — System Tray

**Tanggung jawab:** Bar taskbar di bawah layar, tombol START dengan efek hover, dan label system tray.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Komponen | Deskripsi |
|-----------------|----------|-----------|
| `TASKBAR`, `START_BLUE`, `START_BLUE_HOVER` | Warna | Palet warna taskbar dan tombol START |
| `get_layout()` — `taskbar_top` & `start_rect` | Layout | Hitung posisi taskbar (58px dari bawah) dan area tombol START |
| `draw_ui()` — blok taskbar | Render | Gambar bar taskbar, tombol START (ikon + teks), dan label "WINAPI / GDI" |
| State: `start_hover` | State global | Boolean apakah kursor sedang di atas tombol START |
| `wnd_proc()` — `WM_MOUSEMOVE` (bagian START) | Event | Update `start_hover`, ubah warna tombol START saat hover |
| `wnd_proc()` — `WM_LBUTTONDOWN` (bagian START) | Event | Toggle `menu_open` saat tombol START diklik |
| `get_client_size()` | Helper | Ambil lebar & tinggi area jendela (dipakai taskbar untuk posisi responsif) |

**Konsep yang perlu dipahami:**
- Kenapa taskbar dihitung dari bawah: `taskbar_top = height - 58`
- Efek hover: warna berubah dari `START_BLUE` → `START_BLUE_HOVER` hanya dengan mengubah `start_hover` lalu `InvalidateRect`
- Label `taskbar_label_x = max(150, width - 190)` — label kanan taskbar menyesuaikan lebar jendela

---

### 🖱️ Figa — Event Interaction

**Tanggung jawab:** Semua logika event handling, penanganan keyboard & mouse, dan setup program utama (message loop).

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Komponen | Deskripsi |
|-----------------|----------|-----------|
| `wnd_proc()` — `WM_PAINT` | Event handler | Panggil `draw_ui` setiap kali layar perlu digambar ulang |
| `wnd_proc()` — `WM_ERASEBKGND` | Event handler | Cegah flickering dengan mengembalikan `1` |
| `wnd_proc()` — `WM_KEYDOWN` | Event handler | Tangani Enter/Escape (tutup dialog), Backspace (hapus karakter input) |
| `wnd_proc()` — `WM_CHAR` | Event handler | Tangkap karakter yang diketik ke `dialog_input` |
| `wnd_proc()` — `WM_MOUSEMOVE` | Event handler | Update state hover untuk tombol START dan item menu |
| `wnd_proc()` — `WM_LBUTTONDOWN` | Event handler | Tangani semua klik: dialog OK, START, item menu |
| `wnd_proc()` — `WM_DESTROY` | Event handler | Kirim sinyal keluar saat jendela ditutup |
| `main()` | Entry point | Setup WNDCLASS, daftarkan jendela, buat jendela, jalankan message loop |
| `wnd_proc_callback` | Variabel global | Menyimpan WNDPROC callback agar tidak dihapus garbage collector |
| Semua deklarasi `argtypes` / `restype` | Setup WinAPI | Definisikan tipe parameter & return value semua fungsi DLL |

**Konsep yang perlu dipahami:**
- Message loop: `GetMessageW` → `TranslateMessage` → `DispatchMessageW`
- Sistem prioritas dialog: `msg_dialog_open` > `dialog_open` > interaksi normal
- Kenapa `wnd_proc_callback` harus disimpan di variabel global (garbage collector Python)
- Siklus `InvalidateRect` → `WM_PAINT` → `draw_ui`
- `TranslateMessage` mengubah `WM_KEYDOWN` menjadi `WM_CHAR` untuk input teks

---

### 📋 Rico — Start Menu & Skeleton Graphics

**Tanggung jawab:** Kerangka dasar program (struktur, tipe data, konstanta), panel start menu, daftar item, dan aksi tiap item.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Komponen | Deskripsi |
|-----------------|----------|-----------|
| Load DLL | `user32`, `gdi32`, `kernel32` | Memuat library Windows ke Python |
| Semua konstanta Windows | `WM_*`, `VK_*`, `WS_*`, `CS_*`, dll. | Konstanta numerik Windows API |
| Semua struct | `POINT`, `RECT`, `PAINTSTRUCT`, `MSG`, `WNDCLASS` | Tipe data struktur C yang dipakai WinAPI |
| Tipe data ctypes | `HWND`, `HDC`, `HBRUSH`, `BOOL`, `DWORD`, dll. | Definisi ulang tipe data Windows untuk Python |
| `MENU_ITEMS` | Konstanta | Tuple nama item menu: File, Calculator, Notes, Settings, About, Exit |
| `ITEM`, `ITEM_HOVER`, `HEADER_BLUE`, `PANEL` | Warna | Palet warna panel start menu |
| `get_layout()` | Fungsi layout | Hitung posisi panel, setiap item menu, taskbar_top, dan start_rect |
| `draw_ui()` — blok `if menu_open:` | Render | Gambar panel, header biru, dan semua item menu dengan ikon |
| `run_menu_action()` | Logika aksi | Eksekusi fungsi yang sesuai saat item menu diklik |
| `wnd_proc()` — `WM_LBUTTONDOWN` (bagian menu) | Event | Deteksi klik item menu, jalankan `run_menu_action` |
| `wnd_proc()` — `WM_MOUSEMOVE` (bagian hover item) | Event | Update `hover_index` saat kursor di atas item menu |
| State: `menu_open`, `hover_index` | State global | Status buka/tutup menu dan item yang sedang di-hover |

**Konsep yang perlu dipahami:**
- Cara `hover_index` mengganti warna item: `ITEM_HOVER` jika `index == hover_index`, selain itu `ITEM`
- Kenapa ikon "Exit" berwarna merah (`EXIT_RED`) sedangkan yang lain biru (`ICON_BLUE`)
- `get_layout` menghitung posisi item secara loop: `first_item_top + index * 52`
- Kenapa struct seperti `POINT`, `RECT` perlu didefinisikan ulang di Python (ctypes & kompatibilitas 64-bit)

---

## Peta Fungsi Lengkap

```
main.py
│
├── [Rico] Skeleton Graphics — Kerangka & Struktur
│   ├── Load DLL: user32, gdi32, kernel32
│   ├── Semua konstanta (WM_*, VK_*, WS_*, CS_*, dll.)
│   ├── Semua tipe data (BOOL, HWND, HDC, HBRUSH, dll.)
│   └── Semua struct (POINT, RECT, PAINTSTRUCT, MSG, WNDCLASS)
│
├── [Akbar] Popup & Dialog
│   ├── BACKGROUND, ICON_BLUE, TEXT_PRIMARY, TEXT_SECONDARY (warna)
│   ├── draw_ui() → bagian desktop + tile ikon
│   ├── get_input_dialog_layout()
│   ├── draw_input_dialog()
│   ├── open_file_dialog()
│   ├── get_msg_dialog_layout()
│   ├── draw_msg_dialog()
│   └── show_message()
│
├── [Dicky] System Tray
│   ├── TASKBAR, START_BLUE, START_BLUE_HOVER (warna)
│   ├── get_layout() → taskbar_top + start_rect
│   ├── draw_ui() → blok taskbar + tombol START
│   ├── get_client_size()
│   ├── wnd_proc → WM_MOUSEMOVE (hover START)
│   └── wnd_proc → WM_LBUTTONDOWN (klik START)
│
├── [Rico] Start Menu
│   ├── MENU_ITEMS, ITEM, ITEM_HOVER, PANEL, HEADER_BLUE (konstanta & warna)
│   ├── get_layout() → panel_rect + item_rects
│   ├── draw_ui() → blok if menu_open:
│   ├── run_menu_action()
│   ├── wnd_proc → WM_LBUTTONDOWN (klik item menu)
│   └── wnd_proc → WM_MOUSEMOVE (hover item menu)
│
└── [Figa] Event Interaction
    ├── wnd_proc → WM_PAINT, WM_ERASEBKGND
    ├── wnd_proc → WM_KEYDOWN, WM_CHAR
    ├── wnd_proc → WM_LBUTTONDOWN (dialog OK)
    ├── wnd_proc → WM_DESTROY
    ├── wnd_proc_callback (variabel global WNDPROC)
    ├── main() → setup WNDCLASS + CreateWindow + message loop
    └── Semua argtypes / restype deklarasi
```

---

## Komponen Bersama (Semua Anggota Perlu Paham)

Bagian berikut digunakan bersama oleh semua anggota — wajib dipahami semua orang:

| Komponen | Keterangan |
|----------|------------|
| `rgb(r, g, b)` | Konversi warna — dipakai di semua draw function |
| `draw_rect()` | Fungsi gambar kotak — fondasi semua UI |
| `draw_text()` | Fungsi gambar teks — dipakai di mana-mana |
| `point_in_rect()` | Hit-test klik — dipakai di semua event handler |
| `get_x_lparam()` / `get_y_lparam()` | Unpack koordinat mouse dari `lParam` |
| Semua struct (`RECT`, `POINT`, `MSG`, dll.) | Tipe data WinAPI |
| State global (`menu_open`, `dialog_open`, `msg_dialog_open`) | Kontrol tampilan semua layer UI |
