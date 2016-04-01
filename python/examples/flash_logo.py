import time

import razerdriver


devices = razerdriver.find_devices()
if not devices:
    print("No Razer devices found.")
else:
    device = devices[0]
    print("Ctrl-C to exit.")
    while True:
        device.set_logo(True)
        time.sleep(1)
        device.set_logo(False)
        time.sleep(1)
