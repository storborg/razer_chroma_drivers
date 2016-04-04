import time
import string

import razerdriver
from razerdriver.canvas import KeyCanvas, keynames
from razerdriver import animate


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    canvas = KeyCanvas()
    print("Animating keys in order...")
    names = sorted(keynames)
    for keyname in names:
        canvas.set_key(keyname, (255, 0, 0))
        canvas.animate_key(keyname, animate.linear_fade((255, 0, 0),
                                                        (0, 255, 0),
                                                        50))
        device.write_frame(canvas.render())
        canvas.tick()
        time.sleep(0.1)
    while canvas.is_animating():
        device.write_frame(canvas.render())
        canvas.tick()
        time.sleep(0.1)
