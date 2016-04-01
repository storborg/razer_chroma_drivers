import time

import razerdriver

RED = 255, 0, 0
GREEN = 0, 255, 0


def make_alternating_row(size, start=0):
    ret = []
    for ii in range(size):
        if ii % 2 == start:
            ret.append(RED)
        else:
            ret.append(GREEN)
    return ret


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    for ii in range(6):
        rowbuf = make_alternating_row(22, start=ii % 1)
        print("Setting row %d to %r" % (ii, rowbuf))
        device.set_key_row(ii, rowbuf)
