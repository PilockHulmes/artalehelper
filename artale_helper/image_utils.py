import cv2
import numpy as np

def find_image_position(large_image, small_image, method=cv2.TM_CCOEFF_NORMED, threshold=0.6):
    """
    在大图中查找小图的位置
    
    参数:
        large_image: 大图
        small_image: 小图
        method: 匹配方法，默认为cv2.TM_CCOEFF_NORMED
        threshold: 匹配阈值，默认为0.8
        
    返回:
        匹配位置的矩形坐标(x, y, w, h)，如果没有找到返回None
    """

    
    if large_image is None or small_image is None:
        raise ValueError("无法读取图片，请检查路径是否正确")
    
    # 获取小图尺寸
    h, w = small_image.shape[:2]
    
    # 执行模板匹配
    result = cv2.matchTemplate(large_image, small_image, method)
    
    # 根据匹配方法处理结果
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        location = min_loc if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] else max_loc
    else:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        location = max_loc
    
    # 检查匹配质量
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        if min_val > threshold:
            return None
    else:
        if max_val < threshold:
            return None
    
    # 返回矩形坐标(x, y, w, h)
    return (*location, w, h)

def crop_image_from_origin(image, origin_x, origin_y, width, height):
    """
    以指定坐标(origin_x, origin_y)为原点，截取指定宽度和高度的图像区域，截取逻辑比较奇怪
    
    参数:
        image: 原始图像
        origin_x: 原点x坐标
        origin_y: 原点y坐标
        width: 要截取的宽度
        height: 要截取的高度
    
    返回:
        截取后的图像区域
    """
    start_x = origin_x - width
    end_x = origin_x
    start_y = origin_y
    end_y = origin_y + height

    # 确保边界不超过图像尺寸
    h, w = image.shape[:2]
    end_x = min(end_x, w)
    end_y = min(end_y, h)

    # 使用数组切片截取图像区域
    cropped = image[start_y:end_y, start_x:end_x]
    return cropped