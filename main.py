from Arcanoid import *
from threading import *
from HandDetector import *
from Arduino import *
from Timers import *

hand = Hand()
arc = Arcanoid()
serial_port = Serial_Arduino()
timer = Timer()


# def music_off():
#     while 1:
#         serial_port.pull()
#
#
# t9 = Thread(target=music_off)
# t9.start()


while 1:
    # fps = hand.cap.get(cv2.cv2.CAP_PROP_FPS)
    # print(fps)
    # if db.data_from_arduino == "video":
    #     arc.menu_sound.stop()
    if db.step == "wait":
        # if db.data_from_arduino == "video":
        serial_port.pull()
        if db.data_from_arduino == "game":
            db.step = "init"
    elif db.step == "init":
        arc.init()
        db.step = "init_game"
    elif db.step == "init_game":
        arc.__init__()
        db.step = "init_gif"
    elif db.step == "init_gif":
        t1 = Thread(target=timer.timer_gif)
        t1.start()
        db.step = "timer_off"
    elif db.step == "timer_off":
        t2 = Thread(target=timer.timer_off)
        t2.start()
        arc.menu_sound.play()
        db.step = "gif"
    elif db.step == "gif":
        db.wait = True
        arc.gif()
        hand.detect_all()
        if db.hand_start:
            db.hand_start = False
            t3 = Thread(target=timer.timer_game, args=(3,))
            t3.start()
            t4 = Thread(target=arc.delay)
            t4.start()
            db.step = "delay"
            db.wait = False
            arc.menu_sound.stop()

        if not db.hand_here and not db.off:
            arc.menu_sound.stop()
            db.step = "timer_off"
            db.wait = False
            db.off = True
            db.can_play = False
            db.game = False
        elif db.hand_here:
            db.off = False
    elif db.step == "delay":
        hand.detect_one()
        if db.game:
            db.step = "game"
            db.can_play = True
            t5 = Thread(target=arc.run)
            t5.start()

    elif db.step == "timer_one_off":
        t2 = Thread(target=timer.timer_off)
        t2.start()
        db.step = "game"

    elif db.step == "game":
        hand.detect_one()

        if db.win_or_lose == 1:
            db.step = "win"
        elif db.win_or_lose == 2:
            db.step = "lose"

        if not db.hand_here and not db.off:
            db.step = "init_gif"
            db.wait = False
            db.off = True
            db.can_play = False
            db.game = False
        elif db.hand_here:
            db.off = False

    elif db.step == "win":
        db.wait = False
        db.off = True
        db.can_play = False
        db.game = False
        arc.draw_win()
        db.step = "init_game"
        db.win_or_lose = 0
    elif db.step == "lose":
        db.wait = False
        db.off = True
        db.can_play = False
        db.game = False
        arc.draw_game_over()
        db.step = "init_game"
        db.win_or_lose = 0

    if db.push:
        arc.menu_sound.stop()
        print("qdfjydfjutgrjn64")
        arc.draw_off()
        serial_port.push()
        arc.quit()
        hand.quit()
        db.step = "wait"
        db.data_from_arduino = "video"
        db.game = False
        db.hand_start = False
        db.wait = False
        db.can_play = True
        db.hand_here = True
        db.off = True
        db.push = False
