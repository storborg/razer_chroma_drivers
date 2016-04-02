import os.path
import glob


__version__ = '0.0.1.dev'


def find_devices():
    devices = []
    for devpath in glob.glob('/sys/bus/hid/devices/*'):
        if '1532:020' in devpath:
            if os.path.exists(os.path.join(devpath, 'device_type')):
                device = RazerDevice(devpath)
                devices.append(device)
    return devices


class RazerDevice(object):
    def __init__(self, path):
        self.path = path

    def read_device_file(self, filename):
        fullpath = os.path.join(self.path, filename)
        with open(fullpath, 'rbU') as f:
            ret = f.read()
            return ret

    def write_device_file(self, filename, buf):
        fullpath = os.path.join(self.path, filename)
        with open(fullpath, 'wb') as f:
            f.write(buf)

    def get_device_type(self):
        return self.read_device_file('device_type').strip()

    def get_serial(self):
        return self.read_device_file('get_serial').strip()

    def set_mode_breath(self, primary_color=None, secondary_color=None):
        if primary_color and secondary_color:
            buf = bytearray(primary_color + secondary_color)
        elif primary_color and not secondary_color:
            buf = bytearray(primary_color)
        else:
            buf = b'\x00'
        self.write_device_file('mode_breath', buf)

    def set_mode_none(self):
        self.write_device_file('mode_none', b'\x01')

    def set_mode_reactive(self, speed, color):
        buf = bytearray((speed,) + color)
        self.write_device_file('mode_reactive', buf)

    def set_mode_spectrum(self):
        self.write_device_file('mode_spectrum', b'\x01')

    def set_mode_static(self, color):
        buf = bytearray(color)
        self.write_device_file('mode_static', buf)

    def set_mode_wave(self, direction):
        if direction == 'left':
            buf = b'2'
        elif direction == 'right':
            buf = b'1'
        else:
            raise ValueError("direction must be either 'left' or 'right'")
        self.write_device_file('mode_wave', buf)

    def set_key_row(self, row_index, cols):
        buf = bytearray((row_index,))
        for col in cols:
            buf += bytearray(col)
        self.write_device_file('set_key_row', buf)

    def set_custom_mode(self):
        self.write_device_file('mode_custom', b'1')

    def set_brightness(self, value):
        self.write_device_file('set_brightness', b'%d' % value)

    def set_logo(self, state):
        if state:
            buf = b'1'
        else:
            buf = b'0'
        self.write_device_file('set_logo', buf)

    def write_frame(self, frame):
        assert len(frame) == 6
        for idx, row in enumerate(frame):
            if len(row) < 22:
                pad = [(0, 0, 0)] * (22 - len(row))
                row.extend(pad)
            self.set_key_row(idx, row)
        self.set_custom_mode()
