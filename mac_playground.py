from artale_helper import artale_utils
from artale_helper import image_utils
import cv2
import numpy as np
from PIL import Image
from artale_helper.ocr import OCR

# mac_utils.capture_artale_window()

images, i = artale_utils.get_splited_chat_image()

image = images[0]

# image.show()

ocr = OCR()

ear1 = cv2.imread("./assets/ear1.png", cv2.IMREAD_COLOR)
ear2 = cv2.imread("./assets/ear2.png", cv2.IMREAD_COLOR)
for i, image in enumerate(images):
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    position = image_utils.find_image_position(opencv_image, ear1)
    print(position)
    cropped = image_utils.crop_image_from_origin(opencv_image, position[0], position[1], 57, 24)
    # cv2.imshow("c", cropped)
    # if i == 13:
    rgb_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_img)
    pil_img.show()
    np_image = np.array(pil_img)
    texts = ocr.predict(np_image)
    print(texts)