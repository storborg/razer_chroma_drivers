import time

import razerdriver


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    print("Ctrl-C to exit.")
    while True:
        device.set_mode_static((255, 0, 0))
        time.sleep(1)
        device.set_mode_none()
        time.sleep(1)
