from cvzone.HandTrackingModule import HandDetector
import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

cap = cv2.VideoCapture(1)
detector_one = HandDetector(detectionCon=0.4, maxHands=1)
segmentor = SelfiSegmentation()

while True:
    key = cv2.waitKey(1)
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = segmentor.removeBG(img, (0, 0, 0), threshold=0.1)
    hands, img = detector_one.findHands(img, flipType=False)
    cv2.imshow("qwerty", img)