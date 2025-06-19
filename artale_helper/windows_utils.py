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
    result = list(filter(lambda item: artale_substring in item, titles))
    if len(result) > 0:
        return result[0]
    return ""

def artale_exists():
    return get_artale_title() != ""

def get_artale_window_hwnd():
    return ctypes.windll.user32.FindWindowW(None, get_artale_title())

def force_foreground_window(hwnd):
    """
    强制将窗口带到前台（绕过一些Windows限制）
    """
    # 模拟Alt按键（绕过Windows限制）
    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)  # Alt键按下
    
    # 设置前台窗口
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    
    # 模拟Alt按键释放
    ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)  # Alt键释放
    
    # 恢复窗口（如果最小化）
    if ctypes.windll.user32.IsIconic(hwnd):
        ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9

def maximize_window_safe(hwnd):
    """
    安全地最大化窗口，包含错误检查
    
    参数:
        hwnd: 窗口句柄 (整数)
    返回:
        bool: 是否成功
    """
    if not ctypes.windll.user32.IsWindow(hwnd):
        print("错误: 无效的窗口句柄")
        return False
    
    # 首先确保窗口可见
    if not ctypes.windll.user32.IsWindowVisible(hwnd):
        ctypes.windll.user32.ShowWindow(hwnd, 1)  # SW_SHOWNORMAL = 1
    
    # 先尝试缩小一次，免得窗口卡了导致最大化失败
    ctypes.windll.user32.ShowWindow(hwnd, 2)

    # 最大化窗口 (SW_MAXIMIZE = 3)
    result = ctypes.windll.user32.ShowWindow(hwnd, 3)
    
    return bool(result)

def foreground_artale():
    hwnd = get_artale_window_hwnd()
    if hwnd is not None:
        force_foreground_window(hwnd)
    else:
        print("Artale 窗口不存在")

def maximize_artale():
    hwnd = get_artale_window_hwnd()
    if hwnd is not None:
        maximize_window_safe(hwnd)
    else:
        print("Artale 窗口不存在")