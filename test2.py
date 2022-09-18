import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
from skimage import data, filters

# Open Video
cap = cv2.VideoCapture(1)
detector_one = HandDetector(detectionCon=0.8, maxHands=1)

# Loop over all frames
ret = True
while (ret):
    # Read frame
    ret, frame = cap.read()
    hands, img = detector_one.findHands(frame, flipType=False)
    cv2.imshow('frame', frame)
    cv2.waitKey(20)

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
