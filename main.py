"""Start Menu sederhana yang digambar manual dengan WinAPI dan GDI."""

import ctypes
from ctypes import wintypes


# ---------------------------------------------------------------------------
# Load DLL Windows
# ---------------------------------------------------------------------------

user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


# ---------------------------------------------------------------------------
# Konstanta Windows
# ---------------------------------------------------------------------------

WM_DESTROY = 0x0002
WM_PAINT = 0x000F
WM_ERASEBKGND = 0x0014
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_KEYDOWN = 0x0100
WM_CHAR = 0x0102
WM_KEYUP = 0x0101

VK_BACK = 0x08
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B

CS_VREDRAW = 0x0001
CS_HREDRAW = 0x0002

WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000

SW_SHOW = 5
COLOR_WINDOW = 5
CW_USEDEFAULT = ctypes.c_int(0x80000000).value

IDC_ARROW = 32512
TRANSPARENT = 1
NULL_PEN = 8
DEFAULT_GUI_FONT = 17

# MB_OK dan MB_ICONINFORMATION dihapus — tidak lagi digunakan


# ---------------------------------------------------------------------------
# Fallback tipe data ctypes/wintypes untuk kompatibilitas Windows 64-bit
# ---------------------------------------------------------------------------

BOOL = getattr(wintypes, "BOOL", ctypes.c_int)
BYTE = getattr(wintypes, "BYTE", ctypes.c_ubyte)
WORD = getattr(wintypes, "WORD", ctypes.c_ushort)
UINT = getattr(wintypes, "UINT", ctypes.c_uint)
DWORD = getattr(wintypes, "DWORD", ctypes.c_ulong)
INT = getattr(wintypes, "INT", ctypes.c_int)
LONG = getattr(wintypes, "LONG", ctypes.c_long)

HANDLE = getattr(wintypes, "HANDLE", ctypes.c_void_p)
HWND = getattr(wintypes, "HWND", ctypes.c_void_p)
HINSTANCE = getattr(wintypes, "HINSTANCE", ctypes.c_void_p)
HMODULE = getattr(wintypes, "HMODULE", HINSTANCE)
HICON = getattr(wintypes, "HICON", ctypes.c_void_p)
HCURSOR = getattr(wintypes, "HCURSOR", ctypes.c_void_p)
HBRUSH = getattr(wintypes, "HBRUSH", ctypes.c_void_p)
HDC = getattr(wintypes, "HDC", ctypes.c_void_p)
HMENU = getattr(wintypes, "HMENU", ctypes.c_void_p)
HGDIOBJ = getattr(wintypes, "HGDIOBJ", ctypes.c_void_p)

WPARAM = getattr(wintypes, "WPARAM", ctypes.c_size_t)
LPARAM = getattr(wintypes, "LPARAM", ctypes.c_ssize_t)
LRESULT = getattr(wintypes, "LRESULT", ctypes.c_ssize_t)

LPVOID = getattr(wintypes, "LPVOID", ctypes.c_void_p)
LPCWSTR = getattr(wintypes, "LPCWSTR", ctypes.c_wchar_p)
COLORREF = getattr(wintypes, "COLORREF", DWORD)
ATOM = WORD


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", LONG),
        ("y", LONG),
    ]


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", LONG),
        ("top", LONG),
        ("right", LONG),
        ("bottom", LONG),
    ]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", HDC),
        ("fErase", BOOL),
        ("rcPaint", RECT),
        ("fRestore", BOOL),
        ("fIncUpdate", BOOL),
        ("rgbReserved", BYTE * 32),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
        ("lPrivate", DWORD),
    ]


WNDPROC = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)


class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", INT),
        ("cbWndExtra", INT),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
    ]


# ---------------------------------------------------------------------------
# Deklarasi argtypes dan restype WinAPI
# ---------------------------------------------------------------------------

kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
kernel32.GetModuleHandleW.restype = HMODULE

user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASS)]
user32.RegisterClassW.restype = ATOM

user32.CreateWindowExW.argtypes = [
    DWORD,
    LPCWSTR,
    LPCWSTR,
    DWORD,
    INT,
    INT,
    INT,
    INT,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
]
user32.CreateWindowExW.restype = HWND

user32.ShowWindow.argtypes = [HWND, INT]
user32.ShowWindow.restype = BOOL

user32.UpdateWindow.argtypes = [HWND]
user32.UpdateWindow.restype = BOOL

user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), HWND, UINT, UINT]
user32.GetMessageW.restype = BOOL

user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.TranslateMessage.restype = BOOL

user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.restype = LRESULT

user32.DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
user32.DefWindowProcW.restype = LRESULT

user32.BeginPaint.argtypes = [HWND, ctypes.POINTER(PAINTSTRUCT)]
user32.BeginPaint.restype = HDC

user32.EndPaint.argtypes = [HWND, ctypes.POINTER(PAINTSTRUCT)]
user32.EndPaint.restype = BOOL

user32.InvalidateRect.argtypes = [HWND, ctypes.POINTER(RECT), BOOL]
user32.InvalidateRect.restype = BOOL

user32.GetClientRect.argtypes = [HWND, ctypes.POINTER(RECT)]
user32.GetClientRect.restype = BOOL

user32.LoadCursorW.argtypes = [HINSTANCE, LPCWSTR]
user32.LoadCursorW.restype = HCURSOR

user32.DestroyWindow.argtypes = [HWND]
user32.DestroyWindow.restype = BOOL

user32.PostQuitMessage.argtypes = [INT]
user32.PostQuitMessage.restype = None

user32.MessageBoxW.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
user32.MessageBoxW.restype = INT

gdi32.CreateSolidBrush.argtypes = [COLORREF]
gdi32.CreateSolidBrush.restype = HBRUSH

gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
gdi32.SelectObject.restype = HGDIOBJ

gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DeleteObject.restype = BOOL

gdi32.GetStockObject.argtypes = [INT]
gdi32.GetStockObject.restype = HGDIOBJ

gdi32.Rectangle.argtypes = [HDC, INT, INT, INT, INT]
gdi32.Rectangle.restype = BOOL

gdi32.TextOutW.argtypes = [HDC, INT, INT, LPCWSTR, INT]
gdi32.TextOutW.restype = BOOL

gdi32.SetTextColor.argtypes = [HDC, COLORREF]
gdi32.SetTextColor.restype = COLORREF

gdi32.SetBkMode.argtypes = [HDC, INT]
gdi32.SetBkMode.restype = INT

gdi32.GetTextExtentPoint32W.argtypes = [HDC, LPCWSTR, INT, ctypes.POINTER(POINT)]
gdi32.GetTextExtentPoint32W.restype = BOOL

user32.GetKeyState.argtypes = [INT]
user32.GetKeyState.restype = INT

user32.GetAsyncKeyState.argtypes = [INT]
user32.GetAsyncKeyState.restype = INT


# ---------------------------------------------------------------------------
# State aplikasi dan warna
# ---------------------------------------------------------------------------

MENU_ITEMS = ("File", "Calculator", "Notes", "Settings", "About", "Exit")

menu_open = False
hover_index = -1
start_hover = False
main_hwnd = None
dialog_open = False
dialog_input = ""
dialog_confirmed = False

# State untuk custom info/message dialog (pengganti MessageBoxW)
msg_dialog_open = False
msg_dialog_title = ""
msg_dialog_lines = []  # list of string, hasil split '\n'

BACKGROUND = (24, 27, 34)
TASKBAR = (38, 42, 51)
START_BLUE = (0, 120, 215)
START_BLUE_HOVER = (25, 142, 232)
PANEL = (31, 35, 43)
HEADER_BLUE = (0, 103, 184)
ITEM = (42, 47, 57)
ITEM_HOVER = (61, 68, 82)
TEXT_PRIMARY = (245, 247, 250)
TEXT_SECONDARY = (180, 187, 199)
ICON_BLUE = (58, 151, 240)
EXIT_RED = (195, 62, 70)


# ---------------------------------------------------------------------------
# Fungsi helper
# ---------------------------------------------------------------------------

def rgb(r, g, b):
    """Mengubah RGB menjadi COLORREF Windows (format 0x00BBGGRR)."""
    return r | (g << 8) | (b << 16)


def get_x_lparam(lparam):
    """Mengambil koordinat X bertanda dari LPARAM."""
    return ctypes.c_short(int(lparam) & 0xFFFF).value


def get_y_lparam(lparam):
    """Mengambil koordinat Y bertanda dari LPARAM."""
    return ctypes.c_short((int(lparam) >> 16) & 0xFFFF).value


def draw_rect(hdc, left, top, right, bottom, color):
    """Menggambar kotak berwarna solid menggunakan brush dan Rectangle GDI."""
    brush = gdi32.CreateSolidBrush(rgb(*color))
    if not brush:
        return

    null_pen = gdi32.GetStockObject(NULL_PEN)
    old_brush = gdi32.SelectObject(hdc, brush)
    old_pen = gdi32.SelectObject(hdc, null_pen)

    gdi32.Rectangle(hdc, left, top, right, bottom)

    if old_pen:
        gdi32.SelectObject(hdc, old_pen)
    if old_brush:
        gdi32.SelectObject(hdc, old_brush)
    gdi32.DeleteObject(brush)


def draw_text(hdc, text, x, y, color):
    """Menggambar teks transparan langsung ke device context."""
    gdi32.SetBkMode(hdc, TRANSPARENT)
    gdi32.SetTextColor(hdc, rgb(*color))
    gdi32.TextOutW(hdc, x, y, text, len(text))


def show_message(title, message):
    """Menampilkan custom info dialog yang digambar manual dengan GDI."""
    global msg_dialog_open, msg_dialog_title, msg_dialog_lines
    msg_dialog_title = title
    msg_dialog_lines = message.split("\n")
    msg_dialog_open = True
    user32.InvalidateRect(main_hwnd, None, False)


def open_file_dialog():
    """Buka input dialog untuk nama file (drawn with GDI)."""
    global dialog_open, dialog_input, dialog_confirmed
    dialog_open = True
    dialog_input = ""
    dialog_confirmed = False
    user32.InvalidateRect(main_hwnd, None, False)


def point_in_rect(x, y, rect):
    left, top, right, bottom = rect
    return left <= x < right and top <= y < bottom


def get_client_size(hwnd):
    rect = RECT()
    if not user32.GetClientRect(hwnd, ctypes.byref(rect)):
        return 900, 600
    return max(1, rect.right - rect.left), max(1, rect.bottom - rect.top)


def get_layout(width, height):
    """Membuat semua posisi gambar dan hit-test dari satu sumber data."""
    taskbar_top = max(0, height - 58)
    start_rect = (12, taskbar_top + 10, 132, height - 10)

    panel_left = 12
    panel_right = min(width - 12, 322)
    panel_bottom = max(0, taskbar_top - 8)
    panel_top = max(12, panel_bottom - 386)
    panel_rect = (panel_left, panel_top, panel_right, panel_bottom)

    item_left = panel_left + 10
    item_right = panel_right - 10
    first_item_top = panel_top + 72
    item_rects = []
    for index in range(len(MENU_ITEMS)):
        top = first_item_top + index * 52
        item_rects.append((item_left, top, item_right, top + 44))

    return {
        "taskbar_top": taskbar_top,
        "start_rect": start_rect,
        "panel_rect": panel_rect,
        "item_rects": item_rects,
    }


def get_input_dialog_layout(width, height):
    """Posisi dialog input file yang centered di layar."""
    dialog_width = 350
    dialog_height = 200
    dialog_left = (width - dialog_width) // 2
    dialog_top = (height - dialog_height) // 2
    dialog_right = dialog_left + dialog_width
    dialog_bottom = dialog_top + dialog_height

    label_y = dialog_top + 25
    input_y = dialog_top + 50
    input_height = 35
    ok_btn_y = dialog_bottom - 50
    input_x = dialog_left + 20
    input_width = dialog_width - 40

    ok_btn_left = dialog_left + 80
    ok_btn_right = ok_btn_left + 70
    cancel_btn_left = ok_btn_right + 20
    cancel_btn_right = cancel_btn_left + 70

    return {
        "dialog": (dialog_left, dialog_top, dialog_right, dialog_bottom),
        "label": (input_x, label_y),
        "input": (input_x, input_y, input_x + input_width, input_y + input_height),
        "ok_btn": (ok_btn_left, ok_btn_y, ok_btn_right, ok_btn_y + 35),
        "cancel_btn": (cancel_btn_left, ok_btn_y, cancel_btn_right, ok_btn_y + 35),
    }


def draw_input_dialog(hdc, width, height):
    """Menggambar dialog input file dengan GDI primitives."""
    global dialog_input

    layout = get_input_dialog_layout(width, height)
    dialog_rect = layout["dialog"]
    input_rect = layout["input"]
    ok_rect = layout["ok_btn"]
    cancel_rect = layout["cancel_btn"]

    draw_rect(hdc, *dialog_rect, PANEL)

    draw_rect(
        hdc,
        dialog_rect[0],
        dialog_rect[1],
        dialog_rect[2],
        dialog_rect[1] + 60,
        HEADER_BLUE,
    )
    draw_text(hdc, "Input File Name", dialog_rect[0] + 20, dialog_rect[1] + 10, TEXT_PRIMARY)
    draw_text(hdc, "nama file:", dialog_rect[0] + 20, dialog_rect[1] + 32, (200, 200, 200))

    draw_rect(hdc, *input_rect, (50, 50, 50))
    draw_rect(hdc, input_rect[0] + 2, input_rect[1] + 2, input_rect[2] - 2, input_rect[3] - 2, (70, 70, 70))
    draw_text(hdc, dialog_input + "_", input_rect[0] + 10, input_rect[1] + 8, TEXT_PRIMARY)

    draw_rect(hdc, *ok_rect, START_BLUE)
    draw_text(hdc, "OK", ok_rect[0] + 20, ok_rect[1] + 8, TEXT_PRIMARY)

    draw_rect(hdc, *cancel_rect, (100, 100, 100))
    draw_text(hdc, "Cancel", cancel_rect[0] + 10, cancel_rect[1] + 8, TEXT_PRIMARY)


# ---------------------------------------------------------------------------
# Custom info/message dialog (pengganti MessageBoxW)
# ---------------------------------------------------------------------------


def get_msg_dialog_layout(width, height, line_count):
    """Hitung posisi custom message dialog berdasarkan jumlah baris teks."""
    line_h = 20
    padding_v = 30
    header_h = 52
    btn_h = 36
    btn_margin = 16

    content_h = max(line_count, 1) * line_h + padding_v * 2
    dialog_h = header_h + content_h + btn_h + btn_margin * 2
    dialog_w = 420

    dlg_left = (width - dialog_w) // 2
    dlg_top = (height - dialog_h) // 2
    dlg_right = dlg_left + dialog_w
    dlg_bottom = dlg_top + dialog_h

    first_line_y = dlg_top + header_h + padding_v

    btn_w = 90
    btn_left = dlg_left + (dialog_w - btn_w) // 2
    btn_top = dlg_bottom - btn_margin - btn_h
    btn_right = btn_left + btn_w
    btn_bottom = btn_top + btn_h

    return {
        "dialog": (dlg_left, dlg_top, dlg_right, dlg_bottom),
        "header": (dlg_left, dlg_top, dlg_right, dlg_top + header_h),
        "first_line_y": first_line_y,
        "line_h": line_h,
        "text_x": dlg_left + 24,
        "ok_btn": (btn_left, btn_top, btn_right, btn_bottom),
    }


def draw_msg_dialog(hdc, width, height):
    """Menggambar custom info/message dialog dengan GDI primitives."""
    global msg_dialog_title, msg_dialog_lines

    layout = get_msg_dialog_layout(width, height, len(msg_dialog_lines))
    dlg = layout["dialog"]
    hdr = layout["header"]
    ok = layout["ok_btn"]
    text_x = layout["text_x"]
    line_h = layout["line_h"]
    first_y = layout["first_line_y"]

    # Overlay gelap semi-transparan (solid dark layer)
    draw_rect(hdc, 0, 0, width, height, (10, 12, 18))

    # Bodi dialog
    draw_rect(hdc, *dlg, PANEL)

    # Garis aksen kiri (dekorasi)
    draw_rect(hdc, dlg[0], dlg[1], dlg[0] + 4, dlg[3], ICON_BLUE)

    # Header
    draw_rect(hdc, *hdr, HEADER_BLUE)

    # Ikon info di header (kotak kecil berwarna)
    ico_x = hdr[0] + 16
    ico_y = hdr[1] + (hdr[3] - hdr[1] - 20) // 2
    draw_rect(hdc, ico_x, ico_y, ico_x + 20, ico_y + 20, TEXT_PRIMARY)
    draw_rect(hdc, ico_x + 7, ico_y + 7, ico_x + 13, ico_y + 13, HEADER_BLUE)

    # Judul dialog di header
    draw_text(hdc, msg_dialog_title, hdr[0] + 48, hdr[1] + 16, TEXT_PRIMARY)

    # Garis pemisah tipis di bawah header
    draw_rect(hdc, dlg[0] + 4, hdr[3], dlg[2], hdr[3] + 2, ICON_BLUE)

    # Baris-baris teks konten
    for i, line in enumerate(msg_dialog_lines):
        y = first_y + i * line_h
        if line.strip():
            draw_text(hdc, line, text_x, y, TEXT_SECONDARY)

    # Separator atas tombol OK
    draw_rect(hdc, dlg[0] + 4, ok[1] - 12, dlg[2], ok[1] - 10, (50, 56, 68))

    # Tombol OK
    draw_rect(hdc, *ok, START_BLUE)
    # Teks OK di tengah tombol
    ok_mid_x = ok[0] + (ok[2] - ok[0] - 16) // 2
    ok_mid_y = ok[1] + (ok[3] - ok[1] - 16) // 2
    draw_text(hdc, "OK", ok_mid_x, ok_mid_y, TEXT_PRIMARY)


# ---------------------------------------------------------------------------
# Proses menggambar seluruh antarmuka
# ---------------------------------------------------------------------------

def draw_ui(hwnd, hdc):
    width, height = get_client_size(hwnd)
    layout = get_layout(width, height)

    default_font = gdi32.GetStockObject(DEFAULT_GUI_FONT)
    old_font = gdi32.SelectObject(hdc, default_font)

    # Desktop sederhana.
    draw_rect(hdc, 0, 0, width, height, BACKGROUND)
    draw_text(hdc, "GRAFIKA DESKTOP", 34, 28, TEXT_PRIMARY)
    draw_text(hdc, "Python 3 + WinAPI + GDI", 34, 52, TEXT_SECONDARY)

    desktop_tiles = (
        (34, 96, "PROJECT"),
        (34, 176, "FILES"),
        (34, 256, "SYSTEM"),
    )
    for tile_x, tile_y, label in desktop_tiles:
        draw_rect(hdc, tile_x, tile_y, tile_x + 48, tile_y + 48, (47, 53, 64))
        draw_rect(hdc, tile_x + 12, tile_y + 12, tile_x + 36, tile_y + 36, ICON_BLUE)
        draw_text(hdc, label, tile_x + 60, tile_y + 16, TEXT_SECONDARY)

    # Taskbar dan tombol START.
    taskbar_top = layout["taskbar_top"]
    draw_rect(hdc, 0, taskbar_top, width, height, TASKBAR)

    start_rect = layout["start_rect"]
    start_color = START_BLUE_HOVER if start_hover else START_BLUE
    draw_rect(hdc, *start_rect, start_color)
    draw_rect(
        hdc,
        start_rect[0] + 14,
        start_rect[1] + 9,
        start_rect[0] + 29,
        start_rect[1] + 24,
        TEXT_PRIMARY,
    )
    draw_text(hdc, "START", start_rect[0] + 40, start_rect[1] + 10, TEXT_PRIMARY)

    taskbar_label_x = max(150, width - 190)
    draw_text(hdc, "WINAPI / GDI", taskbar_label_x, taskbar_top + 20, TEXT_SECONDARY)

    if menu_open:
        panel_rect = layout["panel_rect"]
        draw_rect(hdc, *panel_rect, PANEL)

        header_bottom = panel_rect[1] + 62
        draw_rect(
            hdc,
            panel_rect[0],
            panel_rect[1],
            panel_rect[2],
            header_bottom,
            HEADER_BLUE,
        )
        draw_text(
            hdc,
            "START MENU",
            panel_rect[0] + 20,
            panel_rect[1] + 14,
            TEXT_PRIMARY,
        )
        draw_text(
            hdc,
            "Grafika Computer Final Project",
            panel_rect[0] + 20,
            panel_rect[1] + 36,
            (218, 234, 248),
        )

        for index, (label, item_rect) in enumerate(
            zip(MENU_ITEMS, layout["item_rects"])
        ):
            item_color = ITEM_HOVER if index == hover_index else ITEM
            draw_rect(hdc, *item_rect, item_color)

            icon_color = EXIT_RED if label == "Exit" else ICON_BLUE
            icon_left = item_rect[0] + 12
            icon_top = item_rect[1] + 10
            draw_rect(
                hdc,
                icon_left,
                icon_top,
                icon_left + 24,
                icon_top + 24,
                icon_color,
            )
            draw_text(
                hdc,
                label,
                item_rect[0] + 52,
                item_rect[1] + 13,
                TEXT_PRIMARY,
            )

    if dialog_open:
        draw_input_dialog(hdc, width, height)

    if msg_dialog_open:
        draw_msg_dialog(hdc, width, height)

    if old_font:
        gdi32.SelectObject(hdc, old_font)


def run_menu_action(index):
    if index == 0:
        open_file_dialog()
    elif index == 1:
        show_message(
            "Calculator",
            "Kalkulator sederhana\n\nContoh perhitungan:\n125 + 75 = 200",
        )
    elif index == 2:
        show_message(
            "Notes",
            "Notes sederhana\n\n- Final Project Grafika Komputer\n"
            "- GUI digambar manual dengan GDI",
        )
    elif index == 3:
        show_message(
            "Settings",
            "Tema: Dark Modern\nResolusi awal: 900 x 600\nRenderer: Windows GDI",
        )
    elif index == 4:
        show_message(
            "About",
            "Grafika Start Menu\n\nDibuat dengan Python 3, ctypes, "
            "WinAPI, dan GDI.\nTanpa library GUI eksternal.",
        )
    elif index == 5:
        user32.DestroyWindow(main_hwnd)


# ---------------------------------------------------------------------------
# Window procedure
# ---------------------------------------------------------------------------

def wnd_proc(hwnd, msg, wparam, lparam):
    global menu_open, hover_index, start_hover, dialog_open, dialog_input, dialog_confirmed
    global msg_dialog_open, msg_dialog_title, msg_dialog_lines

    if msg == WM_PAINT:
        paint = PAINTSTRUCT()
        hdc = user32.BeginPaint(hwnd, ctypes.byref(paint))
        if hdc:
            draw_ui(hwnd, hdc)
        user32.EndPaint(hwnd, ctypes.byref(paint))
        return 0

    if msg == WM_ERASEBKGND:
        return 1

    if msg == WM_KEYDOWN:
        # Prioritas 1: tutup msg_dialog (info dialog) dengan Enter atau Escape
        if msg_dialog_open:
            if wparam in (VK_RETURN, VK_ESCAPE):
                msg_dialog_open = False
                msg_dialog_title = ""
                msg_dialog_lines = []
                user32.InvalidateRect(hwnd, None, False)
            return 0

        if dialog_open:
            if wparam == VK_BACK:
                if dialog_input:
                    dialog_input = dialog_input[:-1]
                user32.InvalidateRect(hwnd, None, False)
                return 0
            elif wparam == VK_RETURN:
                if dialog_input:
                    dialog_confirmed = True
                    dialog_open = False
                    show_message(
                        "File Berhasil Dibuat",
                        f"File '{dialog_input}' telah dibuat.\n\n"
                        "File ini adalah demo dari input field.\n"
                        "Gunakan untuk project Grafika Komputer Anda.",
                    )
                user32.InvalidateRect(hwnd, None, False)
                return 0
            elif wparam == VK_ESCAPE:
                dialog_open = False
                dialog_input = ""
                user32.InvalidateRect(hwnd, None, False)
                return 0

    if msg == WM_CHAR:
        if dialog_open:
            if 32 <= wparam <= 126:
                if len(dialog_input) < 50:
                    dialog_input += chr(wparam)
                user32.InvalidateRect(hwnd, None, False)
            return 0

    if msg == WM_MOUSEMOVE:
        x = get_x_lparam(lparam)
        y = get_y_lparam(lparam)
        width, height = get_client_size(hwnd)

        if msg_dialog_open:
            return 0

        if dialog_open:
            return 0

        layout = get_layout(width, height)
        new_start_hover = point_in_rect(x, y, layout["start_rect"])
        new_hover_index = -1
        if menu_open:
            for index, item_rect in enumerate(layout["item_rects"]):
                if point_in_rect(x, y, item_rect):
                    new_hover_index = index
                    break

        if new_start_hover != start_hover or new_hover_index != hover_index:
            start_hover = new_start_hover
            hover_index = new_hover_index
            user32.InvalidateRect(hwnd, None, False)
        return 0

    if msg == WM_LBUTTONDOWN:
        x = get_x_lparam(lparam)
        y = get_y_lparam(lparam)
        width, height = get_client_size(hwnd)

        # Prioritas 1: tangani klik di msg_dialog (info dialog)
        if msg_dialog_open:
            msg_layout = get_msg_dialog_layout(width, height, len(msg_dialog_lines))
            if point_in_rect(x, y, msg_layout["ok_btn"]):
                msg_dialog_open = False
                msg_dialog_title = ""
                msg_dialog_lines = []
                user32.InvalidateRect(hwnd, None, False)
            return 0

        if dialog_open:
            dlg_layout = get_input_dialog_layout(width, height)
            if point_in_rect(x, y, dlg_layout["ok_btn"]):
                if dialog_input:
                    dialog_confirmed = True
                    dialog_open = False
                    show_message(
                        "File Berhasil Dibuat",
                        f"File '{dialog_input}' telah dibuat.\n\n"
                        "File ini adalah demo dari input field.\n"
                        "Gunakan untuk project Grafika Komputer Anda.",
                    )
                    dialog_input = ""
            elif point_in_rect(x, y, dlg_layout["cancel_btn"]):
                dialog_open = False
                dialog_input = ""
            user32.InvalidateRect(hwnd, None, False)
            return 0

        layout = get_layout(width, height)

        if point_in_rect(x, y, layout["start_rect"]):
            menu_open = not menu_open
            hover_index = -1
            user32.InvalidateRect(hwnd, None, False)
            return 0

        if menu_open:
            clicked_index = -1
            for index, item_rect in enumerate(layout["item_rects"]):
                if point_in_rect(x, y, item_rect):
                    clicked_index = index
                    break

            if clicked_index >= 0:
                menu_open = False
                hover_index = -1
                user32.InvalidateRect(hwnd, None, False)
                user32.UpdateWindow(hwnd)
                run_menu_action(clicked_index)
                return 0

            if not point_in_rect(x, y, layout["panel_rect"]):
                menu_open = False
                hover_index = -1
                user32.InvalidateRect(hwnd, None, False)
                return 0

    if msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0

    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)


# Callback harus disimpan sebagai variabel global agar tidak dibuang garbage collector.
wnd_proc_callback = WNDPROC(wnd_proc)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    global main_hwnd

    instance = kernel32.GetModuleHandleW(None)
    if not instance:
        raise ctypes.WinError(ctypes.get_last_error())

    class_name = "GrafikaStartMenuWindow"
    cursor_resource = ctypes.cast(ctypes.c_void_p(IDC_ARROW), LPCWSTR)

    window_class = WNDCLASS()
    window_class.style = CS_HREDRAW | CS_VREDRAW
    window_class.lpfnWndProc = wnd_proc_callback
    window_class.cbClsExtra = 0
    window_class.cbWndExtra = 0
    window_class.hInstance = instance
    window_class.hIcon = None
    window_class.hCursor = user32.LoadCursorW(None, cursor_resource)
    window_class.hbrBackground = HBRUSH(COLOR_WINDOW + 1)
    window_class.lpszMenuName = None
    window_class.lpszClassName = class_name

    atom = user32.RegisterClassW(ctypes.byref(window_class))
    if not atom:
        raise ctypes.WinError(ctypes.get_last_error())

    main_hwnd = user32.CreateWindowExW(
        0,
        class_name,
        "Grafika Start Menu - Python WinAPI/GDI",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        900,
        600,
        None,
        None,
        instance,
        None,
    )
    if not main_hwnd:
        raise ctypes.WinError(ctypes.get_last_error())

    user32.ShowWindow(main_hwnd, SW_SHOW)
    user32.UpdateWindow(main_hwnd)

    message = MSG()
    while True:
        result = user32.GetMessageW(ctypes.byref(message), None, 0, 0)
        if result == -1:
            raise ctypes.WinError(ctypes.get_last_error())
        if result == 0:
            break
        user32.TranslateMessage(ctypes.byref(message))
        user32.DispatchMessageW(ctypes.byref(message))

    return int(message.wParam)


if __name__ == "__main__":
    raise SystemExit(main())
