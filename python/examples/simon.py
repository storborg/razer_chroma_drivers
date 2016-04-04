"""
A simon game.

Watch the lights, then repeat.
"""

import time
import random
import string
import curses
import collections

import razerdriver

ROWS = 6
COLS = 16


def make_frame_flash(color):
    frame = []
    for yy in range(ROWS):
        row_data = []
        for xx in range(COLS):
            row_data.append(color)
        frame.append(row_data)
    return frame


def make_frame_for_key(ch, color):
    keys = [
        list('               '),
        list(' `1234567890-= '),
        list('  qwertyuiop[]\ '),
        list('  asdfghjkl;\'   '),
        list('  zxcvbnm,./    '),
        list('               '),
    ]
    frame = []
    for key_row in keys:
        row_data = []
        for key in key_row:
            if key == ch:
                row_data.append(color)
            else:
                row_data.append((0, 0, 0))
        frame.append(row_data)
    return frame


class SimonGame:
    def __init__(self, mode):
        self.score = 1
        self.delay = 0.5
        self.mode = mode

        if mode == 'words':
            # make a dict of lists, where each key is a word length
            self.words = collections.defaultdict(list)
            with open('/usr/share/dict/words', 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    self.words[len(word)].append(word)

    def make_sequence(self):
        if self.mode == 'words':
            return random.choice(self.words[self.score])
        else:
            chars = list(string.ascii_lowercase + string.digits +
                         '`-=[]\;\',./')
            return [random.choice(chars) for __ in range(self.score)]

    def dialog(self, screen, s):
        screen.clear()
        xx = (curses.COLS - len(s)) // 2
        yy = (curses.LINES // 2) - 1
        screen.addstr(yy, xx, s)
        screen.refresh()

    def output_sequence(self, screen, device, seq, delay):
        for c in seq:
            # output char to keyboard key
            self.dialog(screen, "Key: %s" % c)
            device.write_frame(make_frame_for_key(c, (0, 255, 0)))
            time.sleep(delay)
            device.write_frame(make_frame_flash((0, 0, 0)))
            time.sleep(delay / 2)

    def check_input_sequence(self, screen, device, seq, delay):
        screen.timeout(round(delay * 1000))
        for c in seq:
            ch = screen.getch()
            ch = chr(ch)
            if ch != c:
                self.dialog(screen, "FAIL! Typed %s, needed %s." % (ch, c))
                return False
        return True

    def loop(self, screen):
        devices = razerdriver.find_devices()
        if not devices:
            print("No Razer devices found.")
        else:
            device = devices[0]
            curses.use_default_colors()
            curses.curs_set(0)

            while True:
                # make a sequence
                seq = self.make_sequence()

                # spit it out to the keyboard
                self.dialog(screen, "Watch the keyboard.")
                device.write_frame(make_frame_flash((255, 255, 255)))
                time.sleep(1)
                device.write_frame(make_frame_flash((0, 0, 0)))
                time.sleep(1)
                self.output_sequence(screen, device, seq, self.delay)

                # check the user's response
                self.dialog(screen, "Your turn.")
                if not self.check_input_sequence(screen, device, seq,
                                                 self.delay * 10):
                    # game over
                    time.sleep(1)
                    device.write_frame(make_frame_flash((255, 0, 0)))
                    self.dialog(screen, "Game Over.")
                    time.sleep(3)
                    screen.timeout(-1)
                    return self.score
                else:
                    self.dialog(screen, "Well done!")
                    device.write_frame(make_frame_flash((0, 255, 0)))
                    self.score += 1
                    time.sleep(2)


if __name__ == '__main__':
    game = SimonGame('chars')
    score = curses.wrapper(game.loop)
    print("Game Over! Score: %d" % score)
