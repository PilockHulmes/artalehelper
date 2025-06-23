import Quartz
import Cocoa
from Foundation import NSURL
from PIL import Image
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
import time

def get_artale_window():
    window_list = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionAll,
        Quartz.kCGNullWindowID
    )
    for window in window_list:
        if window.get("kCGWindowOwnerName", "") != "MapleStory Worlds":
            continue
        bounds = window.get('kCGWindowBounds', {})
        if "Height" not in bounds or bounds["Height"] < 1080:
            continue
        return window

def activate_artale_window():
    workspace = NSWorkspace.sharedWorkspace()
    for app in workspace.runningApplications():
        if app.localizedName() == "MapleStory Worlds":
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            print(app.localizedName())

def capture_artale_window():
    activate_artale_window()
    time.sleep(0.5)
    return capture_window(get_artale_window(), (5, 342, 1330, 561))

def capture_window(target_window, region_rect=None):
    # 获取窗口ID
    window_id = target_window['kCGWindowNumber']

    # 截取窗口图像
    cg_image = Quartz.CGWindowListCreateImage(
        Quartz.CGRectNull,
        Quartz.kCGWindowListOptionIncludingWindow,
        window_id,
        Quartz.kCGWindowImageBoundsIgnoreFraming | Quartz.kCGWindowImageShouldBeOpaque
    )

    # 如果没有指定区域，返回完整窗口截图
    if not region_rect:
        return _cgimage_to_pil(cg_image)

    # 提取目标区域
    x, y, width, height = region_rect
    crop_rect = Quartz.CGRectMake(x, y, width, height)
    cropped_cg_image = Quartz.CGImageCreateWithImageInRect(cg_image, crop_rect)
    if not cropped_cg_image:
        raise Exception("区域裁剪失败")

    return _cgimage_to_pil(cropped_cg_image)

def _cgimage_to_pil(cg_image):
    """将 CGImage 转换为 PIL.Image"""
    width = Quartz.CGImageGetWidth(cg_image)
    height = Quartz.CGImageGetHeight(cg_image)
    bytesperrow = Quartz.CGImageGetBytesPerRow(cg_image)
    data_provider = Quartz.CGImageGetDataProvider(cg_image)
    data = Quartz.CGDataProviderCopyData(data_provider)
    image = Image.frombytes("RGBA", (width, height), data, "raw", "BGRA", bytesperrow)
    return image.convert("RGB")