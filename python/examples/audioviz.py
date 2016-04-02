import sys

import razerdriver
import pyaudio
import numpy
import numpy.fft

CHUNK = 512
BINS = 16

SAMPLE_RATE = 44100


def render(data, scale=0.3, offset=-3):
    # render numpy array to 6 rows x 16 cols array of rgb tuples
    data = (data * scale) + offset
    frame = []
    for row in range(6):
        row_data = []
        for col in range(16):
            if data[col] > row:
                diff = data[col] - row
                val = int(diff * 255)
                if val < 0:
                    val = 0
                elif val > 255:
                    val = 255
                color = val, 0, 0
            else:
                color = 0, 0, 0
            row_data.append(color)
        frame.append(row_data)
    return frame


def find_pulse_device_index(p):
    for idx in range(p.get_device_count()):
        info = p.get_device_info_by_index(idx)
        if info['name'] == 'pulse':
            return idx


def main(args=sys.argv):
    devices = razerdriver.find_devices()
    if not devices:
        print("No Razer devices found.")
        return
    device = devices[0]
    p = pyaudio.PyAudio()
    device_index = find_pulse_device_index(p)

    if not device_index:
        print("No pulseaudio device found.")
        return

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

    print("Running with pulse audio input. Ctrl-C to exit.")
    print("Be sure to use something like pavucontrol to set your pulse input "
          "device to monitor the desired output device.")
    try:
        while True:
            data = stream.read(CHUNK)
            arr = numpy.fromstring(data, dtype=numpy.int16)
            fdata = numpy.fft.rfft(arr)[:CHUNK / 2]
            mag = numpy.log(numpy.absolute(numpy.square(fdata)))
            reshaped = mag.reshape(-1, CHUNK / (2 * BINS))
            binned = numpy.maximum(reshaped.mean(axis=1), 0)
            frame = render(binned)
            device.write_frame(frame)
    finally:
        print("Cleaning up...")
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main()
