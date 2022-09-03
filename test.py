from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np

cap = cv2.VideoCapture(1)
detector_one = HandDetector(detectionCon=0.8, maxHands=1)

bright = contrast = 0


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


keypad = 0
gamma = False
gamma_k = 2.0

while True:
    key = cv2.waitKey(1)
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = apply_brightness_contrast(img, bright, contrast)

    if key == ord('g'):
        gamma = not gamma

    if key == ord('0'):
        keypad = ord('0')

    if key == ord('1'):
        keypad = ord('1')

    if key == ord('2'):
        keypad = ord('2')

    if key == ord('3'):
        keypad = ord('3')

    if key == ord('4'):
        keypad = ord('4')

    if key == ord('5'):
        keypad = ord('5')

    if keypad == ord('0'):
        img = img

    if keypad == ord('1'):
        img = cv2.cvtColor(img, cv2.COLOR_XYZ2BGR)

    if keypad == ord('2'):
        img = cv2.cvtColor(img, cv2.COLOR_XYZ2RGB)

    if keypad == ord('3'):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2XYZ)

    if keypad == ord('4'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)

    if keypad == ord('5'):
        img = cv2.bitwise_not(img)

    if key == ord('q'):
        pass

    if key == ord('w'):
        bright += 1
    elif key == ord('s'):
        bright -= 1

    if key == ord('e'):
        contrast += 1
    elif key == ord('d'):
        contrast -= 1

    if key == ord('r'):
        contrast += 0.2
    elif key == ord('f'):
        contrast -= 0.2

    if gamma:
        img = gammaCorrection(img, 2.2)

    if key == ord('z'):
        print(bright, contrast, chr(keypad), gamma_k)

    hands, img = detector_one.findHands(img, flipType=False)
    cv2.imshow("qwerty", img)
