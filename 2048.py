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
    result = list()
    result = [0]*len(line)
    position = 0
    for entry in line:
        if entry != 0:
            result.insert(position, entry)
            result.remove(0)
            position += 1

    for entry in range(len(result) - 1):
        if result[entry] == result[entry + 1]:
            result[entry] = result[entry] * 2
            result[entry + 1] = 0
            for num in range(len(result) - 1):
                if result[num] != 0:
                    pass
                else:
                    result[num] = result[num + 1]
                    result[num + 1] = 0

    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        
        self.height = grid_height
        self.width = grid_width
        self.grid = list()
        up_tile = list()
        down_tile = list()
        left_tile = list()
        right_tile = list()
        self.score = 0

        for col in range(self.width):
            up_tile.append([0, col])
            down_tile.append([self.height-1, col])
        for row in range(self.height):
            left_tile.append([row, 0])
            right_tile.append([row, self.width-1])
        self.move_tiles = {
            UP: up_tile,
            DOWN: down_tile,
            LEFT: left_tile,
            RIGHT: right_tile}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        GRID = [[0 for dummy_col in range(self.width)]
                   for dummy_row in range(self.height)] 
        self.grid = GRID
        print(self.grid)
        self.new_tile()
        self.new_tile()
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
#        for row in range(self.width):
#            for col in range(self.height):
#                tiles = self.grid[row][col]
#                string_tiles = str(tiles)
#        return string_tiles
        return ""
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        front_tiles = self.move_tiles.get(direction)
        if (direction == UP) or (direction == DOWN):
            lrange = self.height
        else:
            lrange = self.width

        # Take each line and process.
        for line_num in range(len(front_tiles)):
            # Take the first tile(row, col), compute values of line.
            first = front_tiles[line_num]
            input_line_values = []
            for num in range(lrange):
                new_row = first[0] + OFFSETS[direction][0]*num
                new_col = first[1] + OFFSETS[direction][1]*num
                input_line_values.append(self.get_tile(new_row, new_col))
            output_line = merge(input_line_values)
            # Transfer line values into self.grid.
            for num in range(lrange):
                new_row = first[0] + OFFSETS[direction][0]*num
                new_col = first[1] + OFFSETS[direction][1]*num
                self.set_tile(new_row, new_col, output_line[num])
        self.new_tile()        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.
        """
#        random_cell = [(random.randrange(0, self.width)), (random.randrange(0, self.height))]        
        
        zero_list = list()
        for row in range(self.height):
            for col in range(self.width):             
                if self.grid[row][col] == 0:
                    zero_list.append([row, col])
#                    print zero_list
        if len(zero_list) > 0:
            row = random.choice(zero_list)[0]
            col = random.choice(zero_list)[1]
            print("Random cell is ", (row, col))
            list_of_values = [2] * 9 + [4] 
            print(list_of_values)
            value = random.choice(list_of_values)
            self.set_tile(row, col, value)
            print(value)
        else:
            pass
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value
        print(self.grid)
        
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

if __name__ == "__main__":
    game = TwentyFortyEight(4, 4)
    poc_2048_gui.run_gui(game)

