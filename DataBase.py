WIDTH, HEIGHT = 1200, 800
hand = None
screen = None
fps = 60
seconds = 0

data_from_arduino = "video"

step = "wait"

# Коэффициенты
k_screen = 0.8

# 1______2___
win_or_lose = 0

# =====  BOOL  =========
game = False
rule = True
pause = False
hand_start = False
was_init = False

can_play = True
can_hand_one = True
hand_here = True
off = True
push = False
