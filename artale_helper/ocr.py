from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

class OCR:
    def __init__(self, lang=None):
        if lang is not None:
            self.ocr = PaddleOCR(
                text_detection_model_name="PP-OCRv5_mobile_det",
                text_recognition_model_name="PP-OCRv5_mobile_rec",
                ocr_version="PP-OCRv5",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                lang=lang,
            )
        else:
            self.ocr = PaddleOCR(
                text_detection_model_name="PP-OCRv5_mobile_det",
                text_recognition_model_name="PP-OCRv5_mobile_rec",
                ocr_version="PP-OCRv5",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
    
    def predict(self, image):
        # images = self._ensure_images(images)
        result = self.ocr.predict(image)
        texts = []
        for res in result:
              texts.append("".join(res["rec_texts"]))
        return texts

    def _ensure_images(self, images):
            """
            将各种格式的图片输入统一转换为 NumPy 数组的形式
            
            参数:
                images: 可以是以下四种形式之一:
                    1. 单个 PIL.Image 对象
                    2. PIL.Image 对象列表/数组
                    3. 单个 np.ndarray 图片
                    4. np.ndarray 图片数组
            
            返回:
                np.ndarray: 形状为 (N, H, W, C) 的图片数组
            """
            # 情况1: 单个 PIL 图片
            if isinstance(images, Image.Image):
                return [np.array(images)]
            
            # 情况2: PIL 图片列表/数组
            elif isinstance(images, (list, tuple)) and all(isinstance(img, Image.Image) for img in images):
                return [np.array(img) for img in images]
            
            # 情况3: 单个 numpy 数组
            elif isinstance(images, np.ndarray) and images.ndim == 3:  # 假设3维是 (H,W,C)
                return [images]
            
            # 情况4: numpy 数组列表或已经堆叠的数组
            elif isinstance(images, np.ndarray) and images.ndim == 4:  # 已经是 (N,H,W,C)
                return images

            else:
                raise ValueError("不支持的输入格式。必须是: 单个PIL图片、PIL图片列表、单个numpy数组或numpy数组列表")