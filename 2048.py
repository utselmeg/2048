"""
Clone of 2048 game.
"""

import poc_2048_gui
import random
# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    non_zero = [x for x in line if x != 0]
    merged = []
    score = 0
    i = 0
    while i < len(non_zero):
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            merged.append(non_zero[i] * 2)
            score += non_zero[i] * 2
            i += 2
        else:
            merged.append(non_zero[i])
            i += 1
    merged += [0] * (len(line) - len(merged))
    return merged, score

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()

    def reset(self):
        self._grid = [[0 for _ in range(self._width)] for _ in range(self._height)]
        self.score = 0
        self.new_tile()
        self.new_tile()

    def __str__(self):
        return str(self._grid)

    def get_grid_height(self):
        return self._height

    def get_grid_width(self):
        return self._width

    def move(self, direction):
        has_changed = False
        for start_cell in self.get_start_cells(direction):
            temp_line = self.traverse_line(start_cell, OFFSETS[direction])
            original = [self._grid[row][col] for row, col in temp_line]
            merged, gained = merge(original)
            if merged != original:
                has_changed = True
                self.score += gained
                for index, (row, col) in enumerate(temp_line):
                    self._grid[row][col] = merged[index]
        if has_changed:
            self.new_tile()

    def get_start_cells(self, direction):
        if direction == UP:
            return [(0, col) for col in range(self._width)]
        elif direction == DOWN:
            return [(self._height - 1, col) for col in range(self._width)]
        elif direction == LEFT:
            return [(row, 0) for row in range(self._height)]
        elif direction == RIGHT:
            return [(row, self._width - 1) for row in range(self._height)]

    def traverse_line(self, start, offset):
        row, col = start
        delta_row, delta_col = offset
        cells = []
        while 0 <= row < self._height and 0 <= col < self._width:
            cells.append((row, col))
            row += delta_row
            col += delta_col
        return cells

    def new_tile(self):
        empty = [(row, col) for row in range(self._height)
                 for col in range(self._width) if self._grid[row][col] == 0]
        if empty:
            row, col = random.choice(empty)
            self._grid[row][col] = 4 if random.random() < 0.1 else 2

    def set_tile(self, row, col, value):
        self._grid[row][col] = value

    def get_tile(self, row, col):
        return self._grid[row][col]

if __name__ == "__main__":
    game = TwentyFortyEight(4, 4)
    poc_2048_gui.run_gui(game)
