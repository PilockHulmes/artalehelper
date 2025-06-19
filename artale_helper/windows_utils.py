import ctypes
from ctypes import wintypes

# 定义回调函数类型
EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

def list_window_titles():
    titles = []
    # 获取窗口标题的函数
    def get_window_title(hwnd):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    # 枚举窗口的回调函数
    def enum_windows_callback(hwnd, lParam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            title = get_window_title(hwnd)
            titles.append(title)
        return True
    ctypes.windll.user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)
    return titles

def get_artale_title():
    titles = list_window_titles()
    artale_substring = "MapleStory Worlds-Artale"
    return filter(lambda item: artale_substring in item, titles)
