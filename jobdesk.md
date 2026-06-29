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

### 🖥️ Akbar — Popup & Dialog

**Tanggung jawab:** Tampilan area desktop dan sistem dialog input nama file.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Baris | Deskripsi |
|-----------------|-------|-----------|
| Warna desktop | `BACKGROUND`, `ICON_BLUE`, `TEXT_PRIMARY`, `TEXT_SECONDARY` | Palet warna desktop |
| `draw_ui()` — bagian desktop | Blok gambar background + tile ikon | Gambar desktop, judDicky tile ikon (PROJECT, FILES, SYSTEM) |
| `get_input_dialog_layout()` | Fungsi layout dialog | Hitung posisi dialog input file di tengah layar |
| `draw_input_dialog()` | Fungsi render dialog | Gambar dialog: header, input field dengan kursor `_`, tombol OK & Cancel |
| `open_file_dialog()` | Fungsi helper | Buka dialog input file (set state + InvalidateRect) |
| `WM_CHAR` di `wnd_proc` | Event handler | Tangkap karakter yang diketik user ke `dialog_input` |

**Konsep yang perlu dipahami:**
- Cara kerja `draw_rect` dan `draw_text` (GDI primitives)
- Format COLORREF Windows (`rgb()` function)
- Simulasi kursor teks dengan karakter `"_"` di akhir string input

---

### 🖱️ Figa — Interaksi, Popup, Animasi & Main Program

**Tanggung jawab:** Semua logika event handling, custom dialog info (pengganti MessageBox), dan setup program utama.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Baris | Deskripsi |
|-----------------|-------|-----------|
| `get_msg_dialog_layout()` | Fungsi layout | Hitung posisi dialog info secara dinamis sesuai jumlah baris teks |
| `draw_msg_dialog()` | Fungsi render | Gambar dialog info: overlay gelap, header, ikon, konten multi-baris, tombol OK |
| `show_message()` | Fungsi helper | Set state dialog info + trigger gambar ulang |
| `wnd_proc()` — `WM_KEYDOWN` | Event handler | Tangani Enter/Escape untuk tutup dialog, Backspace di input field |
| `wnd_proc()` — `WM_LBUTTONDOWN` | Event handler | Tangani klik: tombol OK dialog info, OK/Cancel input file, item menu |
| `wnd_proc()` — `WM_PAINT` | Event handler | Panggil `draw_ui` setiap kali layar perlu digambar ulang |
| `wnd_proc()` — `WM_DESTROY` | Event handler | Kirim sinyal keluar saat jendela ditutup |
| `main()` | Entry point | Setup WNDCLASS, buat jendela, jalankan message loop |
| Semua deklarasi `argtypes` / `restype` | Setup WinAPI | Definisikan tipe parameter semua fungsi DLL |

**Konsep yang perlu dipahami:**
- Message loop: `GetMessageW` → `TranslateMessage` → `DispatchMessageW`
- Sistem prioritas dialog (msg_dialog > dialog_open > interaksi normal)
- Kenapa `wnd_proc_callback` harus disimpan di variabel global (garbage collector)
- Siklus `InvalidateRect` → `WM_PAINT` → `draw_ui`

---

### 📋 Dicky — Start Menu (Tile / Kotak Aplikasi)

**Tanggung jawab:** Panel start menu, daftar item menu, dan aksi yang dijalankan tiap item.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Baris | Deskripsi |
|-----------------|-------|-----------|
| `MENU_ITEMS` | Konstanta | Tuple berisi nama-nama item menu: File, Calculator, Notes, Settings, About, Exit |
| `ITEM`, `ITEM_HOVER`, `HEADER_BLUE`, `PANEL` | Warna | Palet warna khusus panel start menu |
| `get_layout()` — `panel_rect` & `item_rects` | Layout | Hitung posisi panel dan setiap item menu |
| `draw_ui()` — blok `if menu_open:` | Render | Gambar panel, header, dan semua item menu dengan ikon |
| `run_menu_action()` | Logika aksi | Eksekusi fungsi yang sesuai saat item diklik |
| `wnd_proc()` — `WM_LBUTTONDOWN` (bagian menu) | Event | Deteksi klik pada item menu, jalankan `run_menu_action` |
| `wnd_proc()` — `WM_MOUSEMOVE` (bagian hover) | Event | Update `hover_index` saat kursor di atas item menu |
| State: `menu_open`, `hover_index` | State global | Status buka/tutup menu dan item yang sedang di-hover |

**Konsep yang perlu dipahami:**
- Cara `hover_index` digunakan untuk mengganti warna item yang di-hover (`ITEM` vs `ITEM_HOVER`)
- Kenapa ikon "Exit" berwarna merah (`EXIT_RED`) sedangkan yang lain biru (`ICON_BLUE`)
- Bagaimana `get_layout` menghitung posisi item secara loop: `first_item_top + index * 52`

---

### 🔷 Rico — Taskbar & System Tray

**Tanggung jawab:** Bar taskbar di bawah layar, tombol START dengan efek hover, dan label system tray.

**Bagian kode yang dikerjakan:**

| Fungsi / Bagian | Baris | Deskripsi |
|-----------------|-------|-----------|
| `TASKBAR`, `START_BLUE`, `START_BLUE_HOVER` | Warna | Palet warna taskbar dan tombol START |
| `get_layout()` — `taskbar_top` & `start_rect` | Layout | Hitung posisi taskbar (58px dari bawah) dan area tombol START |
| `draw_ui()` — blok taskbar | Render | Gambar bar taskbar, tombol START (dengan ikon + teks), dan label "WINAPI / GDI" |
| State: `start_hover` | State global | Boolean apakah kursor sedang di atas tombol START |
| `wnd_proc()` — `WM_MOUSEMOVE` (bagian START) | Event | Update `start_hover`, ubah warna tombol START saat hover |
| `wnd_proc()` — `WM_LBUTTONDOWN` (bagian START) | Event | Toggle `menu_open` saat tombol START diklik |
| `get_client_size()` | Helper | Ambil lebar & tinggi area jendela (dipakai taskbar untuk posisi responsif) |

**Konsep yang perlu dipahami:**
- Kenapa taskbar dihitung dari bawah: `taskbar_top = height - 58`
- Efek hover: warna berubah dari `START_BLUE` → `START_BLUE_HOVER` hanya dengan mengubah `start_hover` dan memanggil `InvalidateRect`
- Label `taskbar_label_x = max(150, width - 190)` — label kanan taskbar menyesuaikan lebar jendela

---

## Peta Fungsi Lengkap

```
main.py
│
├── [Akbar] Desktop & Ikon File
│   ├── BACKGROUND, ICON_BLUE, TEXT_PRIMARY, TEXT_SECONDARY (warna)
│   ├── draw_ui() → bagian desktop + tile ikon
│   ├── get_input_dialog_layout()
│   ├── draw_input_dialog()
│   ├── open_file_dialog()
│   └── wnd_proc → WM_CHAR
│
├── [Figa] Interaksi, Popup & Main Program
│   ├── get_msg_dialog_layout()
│   ├── draw_msg_dialog()
│   ├── show_message()
│   ├── wnd_proc → WM_PAINT, WM_KEYDOWN, WM_LBUTTONDOWN (OK dialog), WM_DESTROY
│   ├── main() → setup + message loop
│   └── Semua argtypes / restype deklarasi
│
├── [Dicky] Start Menu
│   ├── MENU_ITEMS, ITEM, ITEM_HOVER, PANEL, HEADER_BLUE (konstanta & warna)
│   ├── get_layout() → panel_rect + item_rects
│   ├── draw_ui() → blok if menu_open:
│   ├── run_menu_action()
│   ├── wnd_proc → WM_LBUTTONDOWN (klik menu)
│   └── wnd_proc → WM_MOUSEMOVE (hover item)
│
└── [Rico] Taskbar & System Tray
    ├── TASKBAR, START_BLUE, START_BLUE_HOVER (warna)
    ├── get_layout() → taskbar_top + start_rect
    ├── draw_ui() → blok taskbar + tombol START
    ├── get_client_size()
    ├── wnd_proc → WM_MOUSEMOVE (hover START)
    └── wnd_proc → WM_LBUTTONDOWN (klik START)
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
| Semua struct (`RECT`, `POINT`, `MSG`, dll.) | Tipe data WinAPI |
| State global (`menu_open`, `dialog_open`, `msg_dialog_open`) | Kontrol tampilan |
