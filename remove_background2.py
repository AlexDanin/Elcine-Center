import io
import cv2
from rembg.bg import remove
import numpy as np
from PIL import Image

cap = cv2.VideoCapture(1)

while 1:
    s, img = cap.read()
    img = remove(img)

    cv2.imshow("qwerty.png", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        pass
