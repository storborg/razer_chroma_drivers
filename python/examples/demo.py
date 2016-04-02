"""
Cycles through a bunch of example modes.
"""

import time

import razerdriver


RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

DELAY = 5


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    print("Using device: %s" % device.get_device_type())
    print("Ctrl-C to exit. Each mode will be showwn for %d seconds." % DELAY)
    while True:
        print("Resetting brightness to 100.")
        device.set_brightness(100)

        print("Switching to breath mode, random colors.")
        device.set_mode_breath()
        time.sleep(DELAY)

        print("Switching to breath mode, single color (red).")
        device.set_mode_breath(RED)
        time.sleep(DELAY)

        print("Switching off (mode: none).")
        device.set_mode_none()
        time.sleep(DELAY)

        print("Switching to breath mode, double color (green/blue).")
        device.set_mode_breath(GREEN, BLUE)
        time.sleep(DELAY)

        print("Switching to reactive mode, slow/blue (type some characters).")
        device.set_mode_reactive(3, BLUE)
        time.sleep(DELAY)

        print("Switching to spectrum mode.")
        device.set_mode_spectrum()
        time.sleep(DELAY)

        print("Switching to static mode, red.")
        device.set_mode_static(RED)
        time.sleep(DELAY)

        print("Switching to wave mode, left direction.")
        device.set_mode_wave('left')
        time.sleep(DELAY)

        print("Switching to wave mode, right direction.")
        device.set_mode_wave('right')
        time.sleep(DELAY)

        print("Switching to static mode, blue.")
        device.set_mode_static(BLUE)
        for value in range(0, 100, 10):
            print("Setting brightness to %d." % value)
            device.set_brightness(value)
            time.sleep(DELAY / 2)
