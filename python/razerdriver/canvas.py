# Note that this is just for the Blade Stealth for now. Other models are
# unknown.
keys = [
    ('', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
     'f11', 'f12', 'ins', 'del'),
    ('', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',
     'backspace', 'backspace'),
    ('tab', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
     '\\'),
    ('caps', 'caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
     'enter', 'enter', 'enter'),
    ('lshift', 'lshift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
     'rshift', 'rshift', 'rshift'),
    ('lctrl', 'lfn', 'win', 'lalt', 'space', 'space', 'space', 'space',
     'space', 'ralt', 'rfn', 'rctrl', 'left', 'up', 'right', 'down'),
]


keynames = []
keymap = {}
for yy, row in enumerate(keys):
    for xx, keyname in enumerate(row):
        if keyname and (keyname not in keynames):
            keynames.append(keyname)
        keymap.setdefault(keyname, []).append((xx, yy))


class KeyCanvas:
    """
    A higher-level interface to a Chroma keyboard. This is intended to make it
    easier to do things like setting color for a named key, animating effects,
    etc.

    Data is stored as a 3D array (list of list of lists). For a 6x16 keyboard
    like the Razer Blade Stealth, it's a 6x16 array of arbitrarily sized lists.
    The highest nesting level represents animations: when the 'tick' is
    advanced, the first element of each key's list is popped off, until there
    is only one element left (it is preserved).
    """
    def __init__(self, data=None, rows=6, cols=16, initial_color=(0, 0, 0)):
        if data:
            assert len(data) == rows
            for row in data:
                assert len(row) == cols
            self.data = data
        else:
            self.data = []
            for __ in range(rows):
                self.data.append([[initial_color]] * cols)

    def render(self):
        out = []
        for row in self.data:
            out_row = []
            for col in row:
                out_row.append(col[0])
            out.append(out_row)
        return out

    def set_position(self, x, y, color):
        self.data[y][x] = [color]

    def set_key(self, key_name, color):
        for x, y in keymap[key_name]:
            self.data[y][x] = [color]

    def animate_position(self, x, y, animation):
        self.data[y][x] = animation

    def animate_key(self, key_name, animation):
        for x, y in keymap[key_name]:
            self.data[y][x] = animation

    def is_animating(self):
        for row in self.data:
            for col in row:
                if len(col) > 1:
                    return True
        return False

    def tick(self):
        """
        Advance animations to the next frame. Note that this mutates the
        existing data, and does not create a new canvas.
        """
        for row in self.data:
            for col in row:
                if len(col) > 1:
                    col.pop(0)
