import time
import random
import curses

import razerdriver


class GameOver(Exception):
    pass


class SnakeGame:
    def __init__(self, rows=6, cols=16):
        self.rows = rows
        self.cols = cols

        self.snake_color = 0, 255, 0
        self.food_color = 255, 0, 0

        self.food = cols / 2, rows / 2
        self.snake = [(0, 0)]
        self.dir = 1, 0

    def render_chroma(self):
        frame = []
        for yy in range(self.rows):
            row_data = []
            for xx in range(self.cols):
                if (xx, yy) in self.snake:
                    frac = self.snake.index((xx, yy)) / len(self.snake)
                    if frac > 0.5:
                        # mostly blue
                        color = 0, round(255 * frac), 255
                    else:
                        # mostly green
                        color = 0, 255, round(255 * frac)
                elif (xx, yy) == self.food:
                    color = self.food_color
                else:
                    color = 0, 0, 0
                row_data.append(color)
            frame.append(row_data)
        return frame

    def render_curses(self, win):
        win.clear()
        for yy in range(self.rows):
            for xx in range(self.cols):
                if (xx, yy) in self.snake:
                    win.addch(yy, xx, curses.ACS_BLOCK)
                elif (xx, yy) == self.food:
                    win.addch(yy, xx, curses.ACS_DIAMOND)

    def random_food_position(self):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) not in self.snake:
                return x, y

    def next_frame(self, new_dir):
        if new_dir:
            # if the new direction is the opposite of current, ignore itA
            if not ((new_dir[0] + self.dir[0] == 0) and
                    (new_dir[1] + self.dir[1] == 0)):
                self.dir = new_dir

        # calculate next occupied pixel
        head = self.snake[0]
        next_pixel = head[0] + self.dir[0], head[1] + self.dir[1]

        # check for collisions with a wall
        # if so, throw an exception to end the game
        if not ((0 <= next_pixel[0] < self.cols) and
                (0 <= next_pixel[1] < self.rows)):
            raise GameOver

        # check for collisions with the snake at next pixel
        if next_pixel in self.snake:
            # if so, throw an exception to end the game
            raise GameOver
        else:
            # if not, extend the snake head into the next pixel
            self.snake.insert(0, next_pixel)

        # check if we just ate the food
        if next_pixel == self.food:
            # if so, make a new food position and leave the tail
            self.food = self.random_food_position()
        else:
            # if not, move the snake tail (by removing it from the list)
            self.snake.pop()


def get_game_window(screen, game):
    begin_x = (curses.COLS - (game.cols + 2)) // 2
    begin_y = (curses.LINES - (game.rows + 2)) // 2
    outline = curses.newwin(game.rows + 2, game.cols + 2, begin_y, begin_x)
    outline.box()
    outline.refresh()
    win = curses.newwin(game.rows, game.cols, begin_y + 1, begin_x + 1)
    return win


def loop(screen):
    devices = razerdriver.find_devices()
    if not devices:
        print("No Razer devices found.")
    else:
        device = devices[0]
        game = SnakeGame()
        curses.use_default_colors()
        curses.curs_set(0)

        screen.clear()
        screen.refresh()
        screen.nodelay(1)
        win = get_game_window(screen, game)

        while True:
            frame = game.render_chroma()
            game.render_curses(win)
            win.refresh()
            device.write_frame(frame)
            dir = {
                curses.KEY_UP: (0, -1),
                curses.KEY_DOWN: (0, 1),
                curses.KEY_RIGHT: (1, 0),
                curses.KEY_LEFT: (-1, 0),
            }.get(screen.getch())
            try:
                game.next_frame(dir)
            except GameOver:
                s = "Game Over! Score: %d" % len(game.snake)
                x = (curses.COLS - len(s)) // 2
                y = curses.LINES - 2
                screen.addstr(y, x, s)
                screen.nodelay(0)
                screen.getch()
                break
            time.sleep(0.25)


if __name__ == '__main__':
    curses.wrapper(loop)
