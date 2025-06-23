from artale_helper import artale_utils
from artale_helper.ocr import OCR
from artale_helper.redis_writer import RedisWriter
import time
import numpy as np


ocr = OCR()
redis_writer = RedisWriter()
while True:
    time.sleep(1)
    images, i = artale_utils.get_splited_chat_image()
    i.show()
    for image in images:
        np_image = np.array(image)
        texts = ocr.predict(np_image)
        for text in texts:
            print(text)
            # redis_writer.store_string(text)