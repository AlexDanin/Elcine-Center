from cvzone.HandTrackingModule import HandDetector
import cv2
import DataBase as db
from time import sleep
from random import choice as ch


class Hand:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector_multy = HandDetector(detectionCon=0.8, maxHands=20)
        self.detector_one = HandDetector(detectionCon=0.6, maxHands=1)
        self.hand_index = 0

        self.hand_speed = 5
        self.hand_count = 0
        self.hand_num = 1

        self.hand_lst = []
        self.hand_img = 0

        self.picture_hand = cv2.imread("img\pointing-up.png", -1)

    def detect_all(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            hands = self.detector_multy.findHands(img, draw=False, flipType=False)

            if hands:
                print(hands)
                for i in range(len(hands)):
                    if self.detector_multy.fingersUp(hands[i]) == [0, 1, 0, 0, 0] or \
                            self.detector_multy.fingersUp(hands[i]) == [1, 1, 0, 0, 0]:
                        print("all")
                        self.hand_index = i
                        db.hand_start = True
                        self.hand_lst = hands[i]['bbox']
                        self.hand_img = img[self.hand_lst[1] - 10: self.hand_lst[1] + self.hand_lst[3] + 10,
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
                                img[y1:y2, x1:x2, c] = (alpha_s * scr[:, :, c] +
                                                        alpha_l * img[y1:y2, x1:x2, c])
                        except Exception:
                            pass

                        # img[hands[i]['bbox'][1] - 10: hands[i]['bbox'][1] + hands[i]['bbox'][3] + 10,
                        # hands[i]['bbox'][0] - 10: hands[i]['bbox'][0] + hands[i]['bbox'][2] + 10] = scr

                #   fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)
                fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)
                # print(fps)
            cv2.imshow("qwerty", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if db.hand_start:
                break

    def detect_one(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            if db.hand_start:
                img = cv2.blur(img, (50, 50))
                img[self.hand_lst[1] - 10: self.hand_lst[1] + self.hand_lst[3] + 10,
                self.hand_lst[0] - 10: self.hand_lst[0] + self.hand_lst[2] + 10] = self.hand_img
            hand, img = self.detector_one.findHands(img, flipType=False)
            if hand:
                db.hand = hand[0]
                db.hand_start = False

                # fps = self.cap.get(cv2.cv2.CAP_PROP_FPS)
                # print(fps)

                # cv2.circle(img, (self.get_pos_finger()[0], self.get_pos_finger()[1]), 10, (200, 0, 200), cv2.FILLED)

            cv2.imshow("qwerty", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        self.cap.release()

    # def get_pos_finger(self):
    #     return db.hand['lmList'][8][:2]

    # def timer(self):
    #     self.hand_count += 1
    #     if self.hand_count % self.hand_speed == 0:
    #         if self.hand_num < 3:
    #             self.hand_num += 1
    #         else:
    #             self.detector = HandDetector(detectionCon=0.8, maxHands=1)
    #             self.start_game_flag = False
    #             print(ch(list(self.hand_index)))
