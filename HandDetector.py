from cvzone.HandTrackingModule import HandDetector
import cv2
import DataBase as db
import numpy as np
from threading import *
import time


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


class Hand:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        db.cam_w = self.cap.get(3)
        db.cam_h = self.cap.get(4)

        self.detector_multy = HandDetector(detectionCon=0.2, maxHands=20)
        self.detector_one = HandDetector(detectionCon=0.1, maxHands=1)
        self.hand_index = 0

        self.hand_speed = 5
        self.hand_count = 0
        self.hand_num = 1

        self.hand_lst = []
        self.hand_img = 0

        self.picture_hand = cv2.imread("img\pointing-up.png", -1)

        self.img = 0

    def detect_all(self):
        while not db.hand_start:
            success, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 1)
            hands = self.detector_multy.findHands(self.img, draw=False, flipType=False)

            if hands:
                # print(hands)
                for i in range(len(hands)):
                    if self.detector_multy.fingersUp(hands[i]) == [0, 1, 0, 0, 0] or \
                            self.detector_multy.fingersUp(hands[i]) == [1, 1, 0, 0, 0]:
                        print("all")
                        self.hand_index = i
                        db.hand_start = True
                        self.hand_lst = hands[i]['bbox']
                        self.hand_img = self.img[self.hand_lst[1] - 10: self.hand_lst[1] + self.hand_lst[3] + 10,
                                        self.hand_lst[0] - 10: self.hand_lst[0] + self.hand_lst[2] + 10]
                    else:
                        scr = cv2.resize(self.picture_hand,
                                         [(hands[i]['bbox'][0] + hands[i]['bbox'][2] + 30) - (hands[i]['bbox'][0] - 30),
                                          (hands[i]['bbox'][1] + hands[i]['bbox'][3] + 30) - (
                                                  hands[i]['bbox'][1] - 30)])
                        if hands[i]['type'] == 'Left':
                            scr = cv2.flip(scr, 1)

                        try:
                            y1, y2 = hands[i]['bbox'][1] - 30, hands[i]['bbox'][1] - 30 + scr.shape[0]
                            x1, x2 = hands[i]['bbox'][0] - 30, hands[i]['bbox'][0] - 30 + scr.shape[1]

                            alpha_s = scr[:, :, 3] / 255.0
                            alpha_l = 1.0 - alpha_s

                            for c in range(0, 3):
                                self.img[y1:y2, x1:x2, c] = (alpha_s * scr[:, :, c] +
                                                             alpha_l * self.img[y1:y2, x1:x2, c])
                        except Exception:
                            pass

                        # img[hands[i]['bbox'][1] - 10: hands[i]['bbox'][1] + hands[i]['bbox'][3] + 10,
                        # hands[i]['bbox'][0] - 10: hands[i]['bbox'][0] + hands[i]['bbox'][2] + 10] = scr
                # fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)
                # print(fps)
                #   fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)

                db.hand_here = True
            else:
                db.hand_here = False

            cv2.imshow("qwerty", self.img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                pass

    def detect_one(self):
        while 1:
            success, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 0)
            # self.img = gammaCorrection(self.img, 2.2) #
            self.img = apply_brightness_contrast(self.img, 100, 60)
            if db.hand_start:
                self.img = cv2.blur(self.img, (100, 100))
                self.img[self.hand_lst[1] - 10: self.hand_lst[1] + self.hand_lst[3] + 10,
                self.hand_lst[0] - 10: self.hand_lst[0] + self.hand_lst[2] + 10] = self.hand_img
            hand, self.img = self.detector_one.findHands(self.img, flipType=False)
            if hand:
                db.hand = hand[0]['lmList'][8][:2]
                db.hand_start = False
                db.hand_here = True

                # fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)
                # print(fps)

                # cv2.circle(img, (self.get_pos_finger()[0], self.get_pos_finger()[1]), 10, (200, 0, 200), cv2.FILLED)

            cv2.imshow("qwerty", self.img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                pass

    # self.cap.release()

    def get_img(self):
        return self.img

    def quit(self):
        cv2.destroyAllWindows()
