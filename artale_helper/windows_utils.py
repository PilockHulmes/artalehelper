import ctypes
from ctypes import wintypes
from PIL import Image

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


# 定义必要的 Windows 常量
SRCCOPY = 0x00CC0020

# 定义必要的 Windows 结构体
class RECT(ctypes.Structure):
    _fields_ = [
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long)
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', ctypes.c_ulong),
        ('biWidth', ctypes.c_long),
        ('biHeight', ctypes.c_long),
        ('biPlanes', ctypes.c_ushort),
        ('biBitCount', ctypes.c_ushort),
        ('biCompression', ctypes.c_ulong),
        ('biSizeImage', ctypes.c_ulong),
        ('biXPelsPerMeter', ctypes.c_long),
        ('biYPelsPerMeter', ctypes.c_long),
        ('biClrUsed', ctypes.c_ulong),
        ('biClrImportant', ctypes.c_ulong)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', ctypes.c_ulong * 3)  # 颜色表，RGB格式通常不需要
    ]

def capture_window_region(hwnd, left, top, right, bottom):
    """
    截取窗口指定区域的截图
    
    参数:
        hwnd: 窗口句柄
        left, top, right, bottom: 要截取的区域坐标(相对于窗口客户区)
    
    返回:
        PIL.Image 对象
    """
    # 获取窗口DC
    hdc_window = ctypes.windll.user32.GetWindowDC(hwnd)
    
    # 创建兼容DC
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    
    # 计算区域宽度和高度
    width = right - left
    height = bottom - top
    
    # 创建位图
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    
    # 选择位图到内存DC
    hdc_old = ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    
    # 执行位块传输
    ctypes.windll.gdi32.BitBlt(
        hdc_mem, 0, 0, width, height,
        hdc_window, left, top, SRCCOPY
    )
    
    # 获取位图信息
    bmpinfo = BITMAPINFO()
    bmpinfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmpinfo.bmiHeader.biWidth = width
    bmpinfo.bmiHeader.biHeight = -height  # 注意这个负号
    bmpinfo.bmiHeader.biPlanes = 1
    bmpinfo.bmiHeader.biBitCount = 32
    bmpinfo.bmiHeader.biCompression = 0  # BI_RGB
    bmpinfo.bmiHeader.biSizeImage = 0
    
    # 使用正确的缓冲区大小
    buffer = (ctypes.c_byte * (width * height * 4))()
    
    # 确保调用成功
    if not ctypes.windll.gdi32.GetDIBits(
        hdc_mem, hbitmap, 0, height,
        buffer, ctypes.byref(bmpinfo),
        0  # DIB_RGB_COLORS
    ):
        raise RuntimeError("GetDIBits failed")
    
    # 清理资源
    ctypes.windll.gdi32.SelectObject(hdc_mem, hdc_old)
    ctypes.windll.gdi32.DeleteObject(hbitmap)
    ctypes.windll.gdi32.DeleteDC(hdc_mem)
    ctypes.windll.user32.ReleaseDC(hwnd, hdc_window)
    
    # 将缓冲区转换为PIL图像
    img = Image.frombuffer(
        'RGBA',
        (width, height),
        buffer,
        'raw', 'BGRA', 0, 1
    )
    
    return img
