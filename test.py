import pygame as pg
import sys
from Arcanoid import Arcanoid
import DataBase as db
from cvzone.HandTrackingModule import HandDetector
import cv2
from threading import Thread

cap = cv2.VideoCapture(0)

detector_one = HandDetector(detectionCon=0.8, maxHands=1)


arc = Arcanoid()
t1 = Thread(target=arc.run)
t1.start()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector_one.findHands(img, flipType=False)

    if hands:
        fps = cap.get(cv2.cv2.CAP_PROP_FPS)
        print(fps)
        db.hand = hands[0]['lmList'][8][:2]

