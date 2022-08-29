WIDTH, HEIGHT = 1600, 1200
hand = (200, 1)
screen = None
fps = 50
seconds = 0

cam_h = 640
cam_w = 480

data_from_arduino = ""

step = "wait"

gif = ['gif/0.png', 'gif/1.png', 'gif/2.png', 'gif/3.png', 'gif/4.png', 'gif/5.png', 'gif/6.png', 'gif/7.png',
       'gif/8.png', 'gif/9.png', 'gif/10.png', 'gif/11.png', 'gif/12.png', 'gif/13.png', 'gif/14.png', 'gif/15.png',
       'gif/16_2.png', 'gif/17_2.png', 'gif/18_2.png', 'gif/19_2.png', 'gif/20_2.png', 'gif/21_2.png']


img = 'gif/0.png'

# Коэффициенты
k_screen = 0.8

# 1______2___
win_or_lose = 0

# =====  BOOL  =========
game = False
lost = True
pause = False
hand_start = False
was_init = False
wait = True
can_play = True
can_hand_one = True
hand_here = True
off = True
push = False

timer_off = True
