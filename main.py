from artale_helper import artale_utils
from artale_helper.ocr import OCR
from artale_helper.redis_writer import RedisWriter
from artale_helper import image_utils
import time
import numpy as np
import re
import cv2
from PIL import Image

ocr = OCR()
ch_ocr = OCR(lang="en")
redis_writer = RedisWriter(host="localhost")
ear1 = cv2.imread("./assets/ear1.png", cv2.IMREAD_COLOR)
while True:
    time.sleep(1)
    images, i = artale_utils.get_splited_chat_image()
    # i.show()
    for image in images:
        np_image = np.array(image)
        texts = ocr.predict(np_image)
        smega = next(iter(texts), "")

        # 获取频道
        ch_text = ""
        # opencv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        # position = image_utils.find_image_position(opencv_image, ear1)
        # if position is not None and len(position) > 0:
        #     cropped_ch = image_utils.crop_image_from_origin(opencv_image, position[0], position[1], 57, 24)
        #     rgb_ch = cv2.cvtColor(cropped_ch, cv2.COLOR_BGR2RGB)
        #     pil_ch = Image.fromarray(rgb_ch)
        #     np_ch = np.array(pil_ch)
        #     ch_texts = ch_ocr.predict(np_ch)
        #     ch_text = next(iter(ch_texts), "")

        all = smega + " " + ch_text
        print(all)
        redis_writer.store_string(all)