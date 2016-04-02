"""
Plays animation files from the ancient Disco Dance Floor project.
https://www.scotttorborg.com/disco-dance-floor/downloads.html
"""

import time
import struct
import sys

import razerdriver


def load_ddf_file(fname, rows=32, cols=16):
    frames = []
    with open(fname, 'rb') as f:
        while True:
            row_data = []
            for ii in range(rows):
                col_data = []
                for jj in range(cols):
                    buf = f.read(3)
                    if len(buf) < 3:
                        return frames
                    r, g, b = struct.unpack('BBB', buf)
                    col_data.append((r, g, b))
                row_data.append(col_data)
            frames.append(row_data)


def crop_frame(frame, rows=6, cols=16):
    # crop the "top left" to keyboard size
    out = []
    for yy in range(rows):
        out_row = []
        for xx in range(cols):
            out_row.append(frame[yy][xx])
        out.append(out_row)
    return out


def main(args=sys.argv):
    if len(args) < 2:
        print("usage: %s <filename.ddf> [delay]" % args[0])
    else:
        frames = load_ddf_file(args[1])
        if len(args) > 2:
            delay = float(args[2])
        else:
            delay = 0.2
        print("Loaded %d animation frames." % len(frames))
        devices = razerdriver.find_devices()
        if not devices:
            print("No Razer devices found.")
        else:
            device = devices[0]
            while True:
                for frame in frames:
                    device.write_frame(crop_frame(frame))
                    time.sleep(delay)


if __name__ == '__main__':
    main()
