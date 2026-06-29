# 📖 Panduan Kode — Grafika Final Project

> Dokumen ini menjelaskan cara kerja `main.py` secara menyeluruh agar seluruh anggota kelompok memahami setiap bagian kode.

---

## Daftar Isi

1. [Gambaran Umum](#1-gambaran-umum)
2. [Cara Menjalankan](#2-cara-menjalankan)
3. [Arsitektur Program](#3-arsitektur-program)
4. [Bagian 1 — Load DLL Windows](#4-bagian-1--load-dll-windows)
5. [Bagian 2 — Konstanta Windows](#5-bagian-2--konstanta-windows)
6. [Bagian 3 — Tipe Data & Struktur](#6-bagian-3--tipe-data--struktur)
7. [Bagian 4 — Deklarasi Fungsi WinAPI](#7-bagian-4--deklarasi-fungsi-winapi)
8. [Bagian 5 — State Aplikasi & Palet Warna](#8-bagian-5--state-aplikasi--palet-warna)
9. [Bagian 6 — Fungsi Helper](#9-bagian-6--fungsi-helper)
10. [Bagian 7 — Layout & Gambar Dialog Input File](#10-bagian-7--layout--gambar-dialog-input-file)
11. [Bagian 8 — Custom Info Dialog (Pengganti MessageBox)](#11-bagian-8--custom-info-dialog-pengganti-messagebox)
12. [Bagian 9 — Menggambar Seluruh UI (`draw_ui`)](#12-bagian-9--menggambar-seluruh-ui-draw_ui)
13. [Bagian 10 — Aksi Menu (`run_menu_action`)](#13-bagian-10--aksi-menu-run_menu_action)
14. [Bagian 11 — Window Procedure (`wnd_proc`)](#14-bagian-11--window-procedure-wnd_proc)
15. [Bagian 12 — Entry Point (`main`)](#15-bagian-12--entry-point-main)
16. [Alur Kerja Program (Flow Diagram)](#16-alur-kerja-program-flow-diagram)
17. [Konsep Kunci yang Perlu Dipahami](#17-konsep-kunci-yang-perlu-dipahami)

---

## 1. Gambaran Umum

Program ini adalah simulasi **Start Menu desktop** bergaya Windows modern, dibuat **100% dari nol** menggunakan:

| Teknologi | Peran |
|-----------|-------|
| **Python 3** | Bahasa pemrograman utama |
| **ctypes** | Jembatan Python → Windows API |
| **user32.dll** | Membuat jendela, menangkap input mouse/keyboard |
| **gdi32.dll** | Menggambar kotak, teks, dan semua elemen visual |
| **kernel32.dll** | Mendapatkan handle aplikasi |

> **Tidak ada library GUI eksternal** (tidak ada tkinter, pygame, PyQt, dsb.). Semua elemen digambar secara manual piksel demi piksel menggunakan perintah GDI.

---

## 2. Cara Menjalankan

```bash
# Pastikan Python 3 sudah terinstall
python main.py
```

**Persyaratan:** Windows 7 ke atas, Python 3.6+. Tidak perlu install library tambahan apapun.

---

## 3. Arsitektur Program

```
main.py
│
├── Load DLL (user32, gdi32, kernel32)
├── Konstanta & Tipe Data Windows
├── State Global (menu_open, dialog_open, dll.)
├── Palet Warna
│
├── Fungsi Helper
│   ├── rgb()              → konversi warna
│   ├── draw_rect()        → gambar kotak
│   ├── draw_text()        → gambar teks
│   ├── point_in_rect()    → hit-test klik
│   └── get_client_size()  → ukuran jendela
│
├── Sistem Layout (hitung posisi elemen)
│   ├── get_layout()               → taskbar + start menu
│   ├── get_input_dialog_layout()  → dialog input file
│   └── get_msg_dialog_layout()    → dialog info/pesan
│
├── Sistem Gambar (render ke layar)
│   ├── draw_ui()           → menggambar seluruh tampilan
│   ├── draw_input_dialog() → dialog input nama file
│   └── draw_msg_dialog()   → dialog info (pengganti MessageBox)
│
├── Logika Aksi
│   ├── show_message()      → buka dialog info
│   ├── open_file_dialog()  → buka dialog input file
│   └── run_menu_action()   → eksekusi item menu yang diklik
│
├── wnd_proc()   ← JANTUNG program, menangani semua event
│
└── main()       ← Entry point, setup & message loop
```

---

## 4. Bagian 1 — Load DLL Windows

```python
user32   = ctypes.WinDLL("user32",   use_last_error=True)
gdi32    = ctypes.WinDLL("gdi32",    use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
```

`ctypes.WinDLL` membuka file `.dll` bawaan Windows dan memuat semua fungsinya ke memori. Parameter `use_last_error=True` memungkinkan kita menangkap kode error Windows jika ada fungsi yang gagal.

| DLL | Fungsi Utama yang Dipakai |
|-----|--------------------------|
| `user32` | `CreateWindowExW`, `GetMessageW`, `BeginPaint`, `InvalidateRect`, dll. |
| `gdi32` | `Rectangle`, `TextOutW`, `CreateSolidBrush`, `SelectObject`, dll. |
| `kernel32` | `GetModuleHandleW` (mendapatkan handle program ini sendiri) |

---

## 5. Bagian 2 — Konstanta Windows

Konstanta adalah angka ajaib yang digunakan Windows API. Kita mendefinisikannya sendiri agar kode mudah dibaca.

### Pesan Window (WM = Window Message)

```python
WM_PAINT      = 0x000F  # Windows meminta kita menggambar ulang layar
WM_ERASEBKGND = 0x0014  # Windows meminta kita menghapus background
WM_MOUSEMOVE  = 0x0200  # Mouse bergerak
WM_LBUTTONDOWN = 0x0201 # Tombol kiri mouse ditekan
WM_KEYDOWN    = 0x0100  # Tombol keyboard ditekan
WM_CHAR       = 0x0102  # Karakter keyboard diterima (untuk input teks)
WM_DESTROY    = 0x0002  # Jendela sedang ditutup
```

### Virtual Key Codes (VK = Virtual Key)

```python
VK_BACK   = 0x08  # Tombol Backspace
VK_RETURN = 0x0D  # Tombol Enter
VK_ESCAPE = 0x1B  # Tombol Escape
```

### Window Style (WS = Window Style)

```python
WS_OVERLAPPEDWINDOW = 0x00CF0000  # Jendela standar dengan title bar + border
WS_VISIBLE          = 0x10000000  # Jendela langsung terlihat saat dibuat
```

### Class Style (CS = Class Style)

```python
CS_HREDRAW = 0x0002  # Gambar ulang saat lebar jendela berubah
CS_VREDRAW = 0x0001  # Gambar ulang saat tinggi jendela berubah
```

---

## 6. Bagian 3 — Tipe Data & Struktur

Karena Python dan C memiliki tipe data berbeda, kita harus mendefinisikan ulang tipe data Windows agar fungsi WinAPI dapat menerima parameter dengan benar.

### Tipe Primitif

```python
BOOL  = ctypes.c_int      # Boolean (0 = False, bukan-0 = True)
DWORD = ctypes.c_ulong    # 32-bit unsigned integer
HWND  = ctypes.c_void_p   # Handle ke sebuah jendela (pointer)
HDC   = ctypes.c_void_p   # Handle ke Device Context (kanvas gambar)
HBRUSH = ctypes.c_void_p  # Handle ke brush (kuas warna)
```

### Struktur Data (Struct)

Struktur adalah kumpulan data yang dipack bersama, persis seperti struct di C.

#### `POINT` — Koordinat 2D
```python
class POINT(ctypes.Structure):
    _fields_ = [("x", LONG), ("y", LONG)]
```

#### `RECT` — Area persegi panjang
```python
class RECT(ctypes.Structure):
    _fields_ = [("left", LONG), ("top", LONG), ("right", LONG), ("bottom", LONG)]
```

#### `PAINTSTRUCT` — Informasi area yang perlu digambar ulang
Diisi otomatis oleh `BeginPaint()`. Kita hanya perlu meneruskannya.

#### `MSG` — Pesan dari sistem operasi
```python
class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd",    HWND),   # Jendela tujuan pesan
        ("message", UINT),   # Jenis pesan (WM_PAINT, WM_KEYDOWN, dll.)
        ("wParam",  WPARAM), # Data tambahan 1
        ("lParam",  LPARAM), # Data tambahan 2
        ("time",    DWORD),  # Waktu pesan dikirim
        ("pt",      POINT),  # Posisi kursor saat pesan dikirim
        ...
    ]
```

#### `WNDCLASS` — Blueprint / template jendela kita
Mendefinisikan semua properti jendela sebelum dibuat:
- `lpfnWndProc` → fungsi yang menangani semua event (wnd_proc)
- `hbrBackground` → warna default background
- `lpszClassName` → nama unik kelas jendela ini

---

## 7. Bagian 4 — Deklarasi Fungsi WinAPI

Sebelum memanggil fungsi dari DLL, kita harus memberi tahu Python:
- **`argtypes`** → tipe parameter yang diterima fungsi
- **`restype`** → tipe nilai yang dikembalikan fungsi

Ini penting agar Python tidak salah mengkonversi tipe data saat memanggil fungsi C.

```python
# Contoh:
gdi32.Rectangle.argtypes = [HDC, INT, INT, INT, INT]
gdi32.Rectangle.restype  = BOOL
# → Fungsi Rectangle menerima: HDC, x1, y1, x2, y2
# → Dan mengembalikan BOOL (berhasil atau tidak)
```

### Fungsi-fungsi Penting

| Fungsi | DLL | Kegunaan |
|--------|-----|----------|
| `GetModuleHandleW` | kernel32 | Mendapatkan handle program ini sendiri |
| `RegisterClassW` | user32 | Mendaftarkan blueprint jendela |
| `CreateWindowExW` | user32 | Membuat jendela baru |
| `ShowWindow` | user32 | Menampilkan jendela |
| `GetMessageW` | user32 | Mengambil pesan dari antrean (message loop) |
| `BeginPaint` / `EndPaint` | user32 | Memulai / mengakhiri sesi menggambar |
| `InvalidateRect` | user32 | Menandai area untuk digambar ulang |
| `CreateSolidBrush` | gdi32 | Membuat kuas warna solid |
| `Rectangle` | gdi32 | Menggambar persegi panjang |
| `TextOutW` | gdi32 | Menggambar teks ke layar |
| `SetTextColor` | gdi32 | Mengatur warna teks |
| `SelectObject` | gdi32 | Memasang brush/pen/font ke Device Context |
| `DeleteObject` | gdi32 | Membebaskan memori GDI object |

---

## 8. Bagian 5 — State Aplikasi & Palet Warna

### State Global

State adalah variabel yang menyimpan "kondisi saat ini" dari aplikasi. Karena `wnd_proc` dipanggil berkali-kali oleh Windows, state harus disimpan di variabel global.

```python
# --- Start Menu ---
menu_open   = False  # True jika panel start menu sedang terbuka
hover_index = -1     # Index item menu yang sedang di-hover (-1 = tidak ada)
start_hover = False  # True jika kursor ada di atas tombol START
main_hwnd   = None   # Handle jendela utama (diisi saat jendela dibuat)

# --- Dialog Input File ---
dialog_open      = False  # True jika dialog input nama file terbuka
dialog_input     = ""     # Teks yang sedang diketik user
dialog_confirmed = False  # True jika user menekan OK

# --- Dialog Info / Pesan ---
msg_dialog_open  = False  # True jika dialog info sedang terbuka
msg_dialog_title = ""     # Judul yang ditampilkan di header dialog
msg_dialog_lines = []     # List baris teks konten dialog
```

### Palet Warna

Semua warna didefinisikan sebagai tuple `(R, G, B)`:

```python
BACKGROUND       = (24,  27,  34 )  # Abu gelap — warna desktop
TASKBAR          = (38,  42,  51 )  # Sedikit lebih terang — taskbar bawah
START_BLUE       = (0,   120, 215)  # Biru Windows — tombol START
START_BLUE_HOVER = (25,  142, 232)  # Biru lebih terang saat hover
PANEL            = (31,  35,  43 )  # Panel start menu
HEADER_BLUE      = (0,   103, 184)  # Header dialog dan panel
ITEM             = (42,  47,  57 )  # Latar item menu
ITEM_HOVER       = (61,  68,  82 )  # Latar item menu saat hover
TEXT_PRIMARY     = (245, 247, 250)  # Teks utama (hampir putih)
TEXT_SECONDARY   = (180, 187, 199)  # Teks sekunder (abu-abu terang)
ICON_BLUE        = (58,  151, 240)  # Ikon biru di setiap item menu
EXIT_RED         = (195, 62,  70 )  # Ikon merah khusus item "Exit"
```

---

## 9. Bagian 6 — Fungsi Helper

Fungsi-fungsi kecil yang dipakai berulang-ulang di seluruh kode.

### `rgb(r, g, b)` — Konversi Warna
```python
def rgb(r, g, b):
    return r | (g << 8) | (b << 16)
```
Windows menyimpan warna dalam format **COLORREF = 0x00BBGGRR** (terbalik dari RGB biasa).
Fungsi ini mengubah tuple `(R, G, B)` menjadi format integer yang dimengerti GDI.

**Contoh:** `rgb(0, 120, 215)` → `0x00D77800`

### `get_x_lparam(lparam)` dan `get_y_lparam(lparam)` — Posisi Mouse
```python
def get_x_lparam(lparam):
    return ctypes.c_short(int(lparam) & 0xFFFF).value

def get_y_lparam(lparam):
    return ctypes.c_short((int(lparam) >> 16) & 0xFFFF).value
```
Saat event mouse diterima, koordinat X dan Y dikemas bersama dalam satu nilai `lParam` 32-bit:
- **16 bit bawah** = koordinat X
- **16 bit atas** = koordinat Y

Kita unpack dengan bit masking (`&`) dan bit shifting (`>>`). Penggunaan `c_short` memastikan nilai negatif (koordinat di luar area tertentu) tetap terbaca benar.

### `draw_rect(hdc, left, top, right, bottom, color)` — Gambar Kotak
```python
def draw_rect(hdc, left, top, right, bottom, color):
    brush = gdi32.CreateSolidBrush(rgb(*color))  # Buat kuas warna
    null_pen = gdi32.GetStockObject(NULL_PEN)     # Pen transparan (tanpa border)
    old_brush = gdi32.SelectObject(hdc, brush)    # Pasang kuas ke kanvas
    old_pen   = gdi32.SelectObject(hdc, null_pen) # Pasang pen ke kanvas
    
    gdi32.Rectangle(hdc, left, top, right, bottom) # Gambar!
    
    gdi32.SelectObject(hdc, old_pen)    # Kembalikan pen lama
    gdi32.SelectObject(hdc, old_brush)  # Kembalikan brush lama
    gdi32.DeleteObject(brush)           # Hapus kuas dari memori
```
> ⚠️ **Penting:** Setiap GDI object (`brush`, `pen`, `font`) yang dibuat **harus dihapus** dengan `DeleteObject` setelah selesai dipakai, agar tidak terjadi memory leak.

Kenapa `NULL_PEN`? Tanpa `NULL_PEN`, fungsi `Rectangle` GDI akan menggambar border 1px di sekitar kotak. Dengan `NULL_PEN`, tidak ada border.

### `draw_text(hdc, text, x, y, color)` — Gambar Teks
```python
def draw_text(hdc, text, x, y, color):
    gdi32.SetBkMode(hdc, TRANSPARENT)    # Teks tanpa kotak background
    gdi32.SetTextColor(hdc, rgb(*color)) # Atur warna teks
    gdi32.TextOutW(hdc, x, y, text, len(text)) # Gambar teks
```
`TRANSPARENT` memastikan background di belakang teks tidak tertimpa warna putih.

### `point_in_rect(x, y, rect)` — Hit-Test Klik
```python
def point_in_rect(x, y, rect):
    left, top, right, bottom = rect
    return left <= x < right and top <= y < bottom
```
Dipakai setiap kali ada klik mouse untuk mengecek apakah posisi klik ada di dalam suatu elemen UI.

### `get_client_size(hwnd)` — Ukuran Area Gambar
```python
def get_client_size(hwnd):
    rect = RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    return max(1, rect.right - rect.left), max(1, rect.bottom - rect.top)
```
"Client area" = bagian dalam jendela (tidak termasuk title bar dan border). Digunakan agar layout selalu menyesuaikan ukuran jendela jika di-resize.

---

## 10. Bagian 7 — Layout & Gambar Dialog Input File

### `get_layout(width, height)` — Posisi Elemen Utama

Fungsi ini menghitung posisi semua elemen UI utama dari ukuran jendela saat ini:

```
┌────────────────────────────────────────────┐
│  Desktop area                              │
│                                            │
│  ┌──────────────┐                          │
│  │ panel_rect   │  ← Start Menu Panel      │
│  │  (menu item) │                          │
│  │  (menu item) │                          │
│  └──────────────┘                          │
├────────────────────────────────────────────┤
│  [START]           WINAPI / GDI  ← Taskbar │
└────────────────────────────────────────────┘
```

Taskbar selalu 58px dari bawah. Start menu panel muncul tepat di atas tombol START. Posisi dihitung ulang setiap frame sehingga responsif saat jendela di-resize.

### `get_input_dialog_layout(width, height)` — Posisi Dialog Input File

Menghitung posisi dialog input nama file yang selalu **centered** di tengah jendela.

```
┌──────────────────────────────┐
│ ████ Input File Name         │  ← Header biru (60px)
│      nama file:              │
├──────────────────────────────┤
│  ┌────────────────────────┐  │
│  │ teks_yang_diketik_  │  │  │  ← Input field (teks + kursor '_')
│  └────────────────────────┘  │
│         [  OK  ] [ Cancel ]  │
└──────────────────────────────┘
```

### `draw_input_dialog(hdc, width, height)` — Render Dialog Input File

Menggambar semua elemen dialog menggunakan `draw_rect` dan `draw_text`:
1. Bodi dialog (warna PANEL)
2. Header biru dengan teks judul dan label
3. Input field: kotak abu-abu + teks `dialog_input + "_"` (underscore sebagai kursor)
4. Tombol OK (biru) dan Cancel (abu-abu)

---

## 11. Bagian 8 — Custom Info Dialog (Pengganti MessageBox)

Ini adalah pengganti dari `user32.MessageBoxW` yang tidak boleh dipakai. Semua dialog info digambar manual dengan GDI.

### `show_message(title, message)` — Membuka Dialog Info

```python
def show_message(title, message):
    global msg_dialog_open, msg_dialog_title, msg_dialog_lines
    msg_dialog_title = title
    msg_dialog_lines = message.split("\n")  # Pecah teks per baris
    msg_dialog_open = True
    user32.InvalidateRect(main_hwnd, None, False)  # Minta gambar ulang
```
Fungsi ini **tidak langsung menggambar** — ia hanya mengubah state, lalu meminta Windows untuk memanggil `WM_PAINT`, yang kemudian akan memanggil `draw_msg_dialog`.

### `get_msg_dialog_layout(width, height, line_count)` — Posisi Dialog Info

Dialog berukuran **dinamis**: tingginya menyesuaikan jumlah baris teks (`line_count`). Lebarnya selalu 420px dan posisinya selalu center.

```
┌──────────────────────────────────────────┐
│ ■ Judul Dialog                           │  ← Header biru (52px)
├──────────────────────────────────────────┤
│   Baris teks 1                           │
│   Baris teks 2          ← Konten         │
│   Baris teks 3                           │
├──────────────────────────────────────────┤
│                [   OK   ]                │
└──────────────────────────────────────────┘
```

### `draw_msg_dialog(hdc, width, height)` — Render Dialog Info

Urutan penggambaran:
1. **Overlay gelap** → `draw_rect` full layar warna `(10, 12, 18)` menutupi semua UI di belakang
2. **Bodi dialog** → kotak PANEL
3. **Aksen kiri** → strip biru 4px di sisi kiri (dekorasi)
4. **Header** → kotak HEADER_BLUE + ikon info (kotak putih kecil) + teks judul
5. **Garis separator** → garis biru 2px di bawah header
6. **Konten** → loop per baris, `draw_text` untuk setiap baris tidak kosong
7. **Separator tombol** → garis tipis di atas tombol OK
8. **Tombol OK** → kotak biru + teks "OK" di tengah

---

## 12. Bagian 9 — Menggambar Seluruh UI (`draw_ui`)

`draw_ui` adalah fungsi master yang menggambar **seluruh tampilan** dari atas ke bawah setiap kali Windows meminta gambar ulang.

```python
def draw_ui(hwnd, hdc):
    # 1. Ambil ukuran jendela dan hitung layout
    width, height = get_client_size(hwnd)
    layout = get_layout(width, height)

    # 2. Pasang font default
    default_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
    old_font = gdi32.SelectObject(hdc, default_font)

    # 3. Gambar background desktop
    draw_rect(hdc, 0, 0, width, height, BACKGROUND)
    draw_text(hdc, "GRAFIKA DESKTOP", ...)
    draw_text(hdc, "Python 3 + WinAPI + GDI", ...)

    # 4. Gambar tile-tile ikon di desktop
    for tile_x, tile_y, label in desktop_tiles:
        draw_rect(...)  # kotak luar
        draw_rect(...)  # kotak ikon dalam (biru)
        draw_text(...)  # label teks

    # 5. Gambar taskbar
    draw_rect(hdc, 0, taskbar_top, width, height, TASKBAR)

    # 6. Gambar tombol START (warna berubah saat hover)
    start_color = START_BLUE_HOVER if start_hover else START_BLUE
    draw_rect(...)  # kotak tombol
    draw_rect(...)  # ikon Windows kecil di tombol
    draw_text(...)  # teks "START"

    # 7. Gambar panel Start Menu (hanya jika menu_open = True)
    if menu_open:
        draw_rect(...)   # bodi panel
        draw_rect(...)   # header biru
        draw_text(...)   # judul "START MENU"
        for each item:
            draw_rect(...)  # latar item (berbeda warna jika di-hover)
            draw_rect(...)  # ikon item
            draw_text(...)  # label item

    # 8. Gambar dialog input file (hanya jika dialog_open = True)
    if dialog_open:
        draw_input_dialog(hdc, width, height)

    # 9. Gambar dialog info (hanya jika msg_dialog_open = True)
    if msg_dialog_open:
        draw_msg_dialog(hdc, width, height)

    # 10. Kembalikan font lama
    gdi32.SelectObject(hdc, old_font)
```

> **Penting:** Urutan penggambaran sangat penting! Elemen yang digambar belakangan akan menutupi elemen sebelumnya. Itulah mengapa overlay dialog digambar paling akhir agar berada di "lapisan" teratas.

---

## 13. Bagian 10 — Aksi Menu (`run_menu_action`)

```python
def run_menu_action(index):
    if index == 0:   open_file_dialog()         # File
    elif index == 1: show_message("Calculator", "...")
    elif index == 2: show_message("Notes", "...")
    elif index == 3: show_message("Settings", "...")
    elif index == 4: show_message("About", "...")
    elif index == 5: user32.DestroyWindow(main_hwnd)  # Exit
```

Dipanggil dari `wnd_proc` saat user mengklik salah satu item di Start Menu. Index sesuai dengan urutan `MENU_ITEMS = ("File", "Calculator", "Notes", "Settings", "About", "Exit")`.

---

## 14. Bagian 11 — Window Procedure (`wnd_proc`)

Ini adalah **jantung** program. Setiap kali terjadi event (mouse bergerak, tombol ditekan, layar perlu digambar ulang), Windows memanggil fungsi ini.

```python
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)

def wnd_proc(hwnd, msg, wparam, lparam):
    # hwnd   = handle jendela yang menerima pesan
    # msg    = jenis pesan (WM_PAINT, WM_KEYDOWN, dll.)
    # wparam = data tambahan (kode tombol, dll.)
    # lparam = data tambahan (koordinat mouse, dll.)
```

### Event yang Ditangani

#### `WM_PAINT` — Gambar ulang layar
```python
if msg == WM_PAINT:
    paint = PAINTSTRUCT()
    hdc = user32.BeginPaint(hwnd, ctypes.byref(paint))
    if hdc:
        draw_ui(hwnd, hdc)   # ← Gambar semua UI
    user32.EndPaint(hwnd, ctypes.byref(paint))
    return 0
```
Harus selalu dipasangkan `BeginPaint` ↔ `EndPaint`.

#### `WM_ERASEBKGND` — Hapus background
```python
if msg == WM_ERASEBKGND:
    return 1  # Bilang ke Windows "sudah aku tangani sendiri"
```
Dengan mengembalikan `1`, kita mencegah Windows menggambar background putih default yang akan menyebabkan flickering.

#### `WM_KEYDOWN` — Tombol ditekan

Urutan prioritas penanganan:
1. Jika **dialog info terbuka** (`msg_dialog_open`) → Enter/Escape tutup dialog
2. Jika **dialog input file terbuka** (`dialog_open`) → Backspace hapus karakter, Enter konfirmasi, Escape batal

```python
if msg == WM_KEYDOWN:
    if msg_dialog_open:          # Dialog info punya prioritas tertinggi
        if wparam in (VK_RETURN, VK_ESCAPE):
            msg_dialog_open = False
            user32.InvalidateRect(hwnd, None, False)
        return 0

    if dialog_open:              # Dialog input file
        if wparam == VK_BACK:    dialog_input = dialog_input[:-1]
        elif wparam == VK_RETURN: # Konfirmasi → tampilkan dialog info
        elif wparam == VK_ESCAPE: dialog_open = False
```

#### `WM_CHAR` — Karakter keyboard

```python
if msg == WM_CHAR:
    if dialog_open:
        if 32 <= wparam <= 126:  # Karakter ASCII yang bisa dicetak
            if len(dialog_input) < 50:
                dialog_input += chr(wparam)
```
Berbeda dari `WM_KEYDOWN`, `WM_CHAR` sudah mengonversi kode tombol menjadi karakter teks. Cocok untuk menangkap input teks yang diketik.

#### `WM_MOUSEMOVE` — Mouse bergerak

```python
if msg == WM_MOUSEMOVE:
    x = get_x_lparam(lparam)
    y = get_y_lparam(lparam)

    if msg_dialog_open: return 0  # Block interaksi saat dialog info terbuka
    if dialog_open: return 0      # Block interaksi saat dialog input terbuka

    # Cek apakah kursor di atas tombol START atau item menu
    new_start_hover = point_in_rect(x, y, layout["start_rect"])
    new_hover_index = ... # loop cek setiap item menu

    # Hanya gambar ulang jika ada perubahan (optimasi)
    if new_start_hover != start_hover or new_hover_index != hover_index:
        start_hover = new_start_hover
        hover_index = new_hover_index
        user32.InvalidateRect(hwnd, None, False)
```

#### `WM_LBUTTONDOWN` — Klik kiri mouse

Urutan prioritas penanganan:
1. **Dialog info terbuka** → klik OK tutup dialog
2. **Dialog input file terbuka** → klik OK konfirmasi, klik Cancel batal
3. **Tidak ada dialog** → klik START toggle menu, klik item menu jalankan aksi, klik di luar panel tutup menu

#### `WM_DESTROY` — Jendela ditutup
```python
if msg == WM_DESTROY:
    user32.PostQuitMessage(0)  # Kirim sinyal keluar ke message loop
    return 0
```

#### Default
```python
return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
```
Semua pesan yang tidak kita tangani diserahkan ke handler default Windows.

### Kenapa Callback Disimpan di Variabel Global?

```python
wnd_proc_callback = WNDPROC(wnd_proc)
```
Python memiliki **garbage collector** yang menghapus objek yang tidak direferensikan. Jika callback disimpan sebagai variabel lokal, Python bisa menghapusnya dari memori sementara Windows masih memanggilnya → crash. Menyimpan di variabel global memastikan callback tetap hidup selama program berjalan.

---

## 15. Bagian 12 — Entry Point (`main`)

Fungsi `main()` bertugas melakukan setup awal dan menjalankan message loop.

```python
def main():
    global main_hwnd

    # Langkah 1: Dapatkan handle aplikasi ini sendiri
    instance = kernel32.GetModuleHandleW(None)

    # Langkah 2: Daftarkan blueprint jendela
    window_class = WNDCLASS()
    window_class.style          = CS_HREDRAW | CS_VREDRAW  # Gambar ulang saat resize
    window_class.lpfnWndProc    = wnd_proc_callback         # Fungsi event handler kita
    window_class.hInstance      = instance
    window_class.hCursor        = user32.LoadCursorW(None, IDC_ARROW)  # Kursor panah
    window_class.hbrBackground  = HBRUSH(COLOR_WINDOW + 1) # Background putih default
    window_class.lpszClassName  = "GrafikaStartMenuWindow"
    user32.RegisterClassW(ctypes.byref(window_class))

    # Langkah 3: Buat jendela
    main_hwnd = user32.CreateWindowExW(
        0,                      # dwExStyle: tidak ada style extended
        "GrafikaStartMenuWindow",  # Nama kelas yang sudah didaftarkan
        "Grafika Start Menu - Python WinAPI/GDI",  # Judul title bar
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,  # Style: jendela standar + langsung tampil
        CW_USEDEFAULT, CW_USEDEFAULT,      # Posisi X, Y (biarkan Windows tentukan)
        900, 600,               # Lebar x Tinggi jendela
        None, None, instance, None
    )

    # Langkah 4: Tampilkan jendela
    user32.ShowWindow(main_hwnd, SW_SHOW)
    user32.UpdateWindow(main_hwnd)

    # Langkah 5: Message Loop — program berjalan di sini sampai ditutup
    message = MSG()
    while True:
        result = user32.GetMessageW(ctypes.byref(message), None, 0, 0)
        if result == -1: raise ctypes.WinError(...)  # Error
        if result == 0:  break                        # WM_QUIT diterima → keluar

        user32.TranslateMessage(ctypes.byref(message))  # Konversi WM_KEYDOWN → WM_CHAR
        user32.DispatchMessageW(ctypes.byref(message))  # Kirim ke wnd_proc

    return int(message.wParam)
```

### Message Loop

```
GetMessageW → ambil pesan dari antrian
     ↓
TranslateMessage → konversi keystroke menjadi WM_CHAR
     ↓
DispatchMessageW → panggil wnd_proc dengan pesan tersebut
     ↓
(kembali ke GetMessageW, ulangi terus sampai WM_QUIT)
```

---

## 16. Alur Kerja Program (Flow Diagram)

```
main()
│
├── Setup jendela
│
└── Message Loop (berjalan terus-menerus)
         │
         ├── [WM_PAINT]
         │       └── draw_ui()
         │               ├── Gambar desktop + taskbar
         │               ├── [jika menu_open] Gambar panel + item
         │               ├── [jika dialog_open] draw_input_dialog()
         │               └── [jika msg_dialog_open] draw_msg_dialog()
         │
         ├── [WM_MOUSEMOVE]
         │       ├── Update start_hover & hover_index
         │       └── InvalidateRect() → picu WM_PAINT
         │
         ├── [WM_LBUTTONDOWN]
         │       ├── Klik tombol OK di msg_dialog → tutup dialog
         │       ├── Klik OK/Cancel di input_dialog → konfirmasi/batal
         │       ├── Klik START → toggle menu_open
         │       └── Klik item menu → run_menu_action()
         │                               ├── show_message() → buka msg_dialog
         │                               ├── open_file_dialog() → buka input_dialog
         │                               └── DestroyWindow() → tutup program
         │
         ├── [WM_KEYDOWN]
         │       ├── [msg_dialog_open] Enter/Esc → tutup msg_dialog
         │       └── [dialog_open] Backspace/Enter/Esc → edit/konfirmasi/batal
         │
         ├── [WM_CHAR]
         │       └── [dialog_open] Tambah karakter ke dialog_input
         │
         └── [WM_DESTROY]
                 └── PostQuitMessage() → akhiri message loop
```

---

## 17. Konsep Kunci yang Perlu Dipahami

### Konsep 1: Device Context (HDC)
HDC adalah "kanvas" GDI. Semua fungsi gambar (`Rectangle`, `TextOutW`, dll.) membutuhkan HDC sebagai parameter pertama. HDC hanya valid antara `BeginPaint` dan `EndPaint`.

### Konsep 2: Immediate Mode Rendering
Program ini menggunakan **immediate mode** — tidak ada "scene graph" atau "widget tree". Setiap kali layar perlu diperbarui, **seluruh UI digambar ulang dari nol** (`draw_ui` dipanggil lagi). Ini berbeda dari framework GUI modern yang hanya mengupdate bagian yang berubah.

### Konsep 3: Invalidate → Paint Cycle
Cara memperbarui tampilan:
```
Ubah state  →  InvalidateRect()  →  Windows kirim WM_PAINT  →  draw_ui()
```
Kita **tidak pernah** menggambar langsung di luar `WM_PAINT`. Semua perubahan visual dilakukan dengan mengubah state lalu memanggil `InvalidateRect`.

### Konsep 4: Z-Order (Lapisan)
Karena semua digambar ke HDC yang sama, urutan penggambaran menentukan "siapa di atas siapa":
- Desktop digambar pertama (paling bawah)
- Taskbar di atas desktop
- Panel menu di atas taskbar  
- Dialog di atas segalanya (digambar terakhir)

### Konsep 5: GDI Object Lifecycle
```
Create Object → Select into HDC → Use → Deselect (select old back) → Delete
```
Setiap objek GDI (brush, pen, font, bitmap) yang dibuat **wajib dihapus** dengan `DeleteObject` untuk menghindari memory leak.

---

*Guide ini dibuat untuk membantu seluruh anggota kelompok memahami arsitektur dan cara kerja `main.py` secara menyeluruh.*
