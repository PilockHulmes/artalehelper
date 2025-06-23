
import ctypes
import time
from PIL import Image
import platform

if platform.system() == "Windows":
    from artale_helper import windows_utils
if platform.system() == "Darwin":
    from artale_helper import mac_utils

def get_artale_title():
    titles = windows_utils.list_window_titles()
    artale_substring = "MapleStory Worlds-Artale"
    result = list(filter(lambda item: artale_substring in item, titles))
    if len(result) > 0:
        return result[0]
    return ""

def get_artale_window_hwnd():
    return ctypes.windll.user32.FindWindowW(None, get_artale_title())

def artale_exists():
    return get_artale_title() != ""

def foreground_artale():
    hwnd = get_artale_window_hwnd()
    if hwnd is not None:
        windows_utils.force_foreground_window(hwnd)
    else:
        print("Artale 窗口不存在")

def maximize_artale():
    hwnd = get_artale_window_hwnd()
    if hwnd is not None:
        windows_utils.maximize_window_safe(hwnd)
    else:
        print("Artale 窗口不存在")

def get_chat_image():
    foreground_artale()
    maximize_artale()
    time.sleep(0.5) # wait for window to show up
    return windows_utils.capture_window_region(0, 5, 379, 1135, 902).convert("RGB")

def split_smega_image_vertically(image, parts=17, part_height=31):
    """
    将喇叭信息垂直分割成指定数量的等份
    :param image: PIL Image 对象
    :param parts: 要分割的份数
    :return: 包含所有分割后图像的列表
    """
    width, height = image.size
    cropped_images = []
    for i in range(parts):
        # 计算每个部分的边界框 (left, upper, right, lower)
        upper = i * part_height
        lower = upper + part_height
        # 处理最后一个部分可能高度不足的情况
        if i == parts - 1:
            lower = height
        # 裁剪图像
        cropped = image.crop((0, upper, width, lower))
        cropped_images.append(cropped)
    return cropped_images

def get_splited_chat_image():
    if platform.system() == "Windows":
        image = get_chat_image()
        return split_smega_image_vertically(image, 17, 31), image
    elif platform.system() == "Darwin":
        image = mac_utils.capture_artale_window()
        return split_smega_image_vertically(image, 17, 33), image