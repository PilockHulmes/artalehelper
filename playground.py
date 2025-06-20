from artale_helper import artale_utils
import time
import numpy as np
from paddleocr import PaddleOCR
import re

images = artale_utils.get_splited_chat_image()
# images[1].show()

# image.show()

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

pattern = r'^(.*?)CH\d+：(.*?)$'

for i, image in enumerate(images):
    image_np = np.array(image)
    result = ocr.predict(input=image_np)
    for res in result:
        # res.save_to_json("output")
        smega_text = "".join(res["rec_texts"])
        m = re.match(pattern, smega_text)
        if m:
            name = m.group(1)
            content = m.group(2)
            print(name, content)
    # print(result)
    # if result is not None and result[0] is not None and len(result) > 0 :
    #     for line in result[0]:
    #         if type(line[1][0]) == str:
    #             print(line[1][0])

# windows_utils.capture_screen()