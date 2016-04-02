import time

import razerdriver

RED = 255, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
BLUE = 0, 0, 255


def make_alternating_row(size, a, b, start=0):
    ret = []
    for ii in range(size):
        if ii % 2 == start:
            ret.append(a)
        else:
            ret.append(b)
    return ret


def draw_frame(device, idx):
    print("frame %d" % idx)
    if idx % 8 > 4:
        x, y = RED, GREEN
    else:
        x, y = YELLOW, BLUE
    if idx % 2 == 1:
        a, b = x, y
    else:
        a, b = y, x
    frame = []
    for ii in range(6):
        frame.append(make_alternating_row(16, a, b, start=ii % 1))
    device.write_frame(frame)


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    for frame in range(600):
        draw_frame(device, frame)
        time.sleep(0.3)
