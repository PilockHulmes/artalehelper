from artale_helper import artale_utils
from artale_helper.ocr import OCR
from artale_helper.redis_writer import RedisWriter
import time


ocr = OCR()
redis_writer = RedisWriter()
while True:
    time.sleep(5)
    images = artale_utils.get_splited_chat_image()
    texts = ocr.predict(images)
    for text in texts:
        redis_writer.store_string(text)