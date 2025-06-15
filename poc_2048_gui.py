import tkinter as tk

TILE_SIZE = 100
TILE_PADDING = 10
FONT = ("Verdana", 24, "bold")
SCORE_FONT = ("Verdana", 16, "bold")
BACKGROUND_COLOR = "#bbada0"
TILE_COLORS = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
    128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    1024: "#edc53f", 2048: "#edc22e"
}

class TwentyFortyEightGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("2048")
        self.canvas_width = TILE_SIZE * game.get_grid_width()
        self.canvas_height = TILE_SIZE * game.get_grid_height() + 50
        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                                height=self.canvas_height, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        self.root.bind("<Key>", self.key_handler)
        self.score_text = self.canvas.create_text(
            self.canvas_width // 2, 25, text="Score: 0",
            font=SCORE_FONT, fill="white"
        )
        self.draw()
        self.root.mainloop()

    def key_handler(self, event):
        direction = {"Up": 1, "Down": 2, "Left": 3, "Right": 4}.get(event.keysym)
        if direction:
            self.game.move(direction)
            self.draw()

    def animate_tile_move(self, x0, y0, x1, y1, text, steps=5):
        tile = self.canvas.create_text(x0, y0, text=text, font=FONT, fill="black")
        dx = (x1 - x0) / steps
        dy = (y1 - y0) / steps
        for _ in range(steps):
            self.canvas.move(tile, dx, dy)
            self.root.update()
            self.root.after(10)
        self.canvas.delete(tile)

    def draw_merge_pop_effect(self, merged_tiles):
        # merged_tiles = list of (row, col, value)
        size_steps = [1.1, 1.3, 1.1, 1.0]
        for scale in size_steps:
            self.canvas.delete("merge_pop")
            for row, col, value in merged_tiles:
                x = col * TILE_SIZE + TILE_SIZE // 2
                y = row * TILE_SIZE + TILE_SIZE // 2 + 50
                color = TILE_COLORS.get(value, "#3c3a32")
                half_size = (TILE_SIZE - TILE_PADDING * 2) * scale / 2
                x0 = x - half_size
                y0 = y - half_size
                x1 = x + half_size
                y1 = y + half_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags="merge_pop")
                self.canvas.create_text(x, y, text=str(value),
                                        font=("Verdana", int(24 * scale), "bold"),
                                        fill="black", tags="merge_pop")
            self.root.update()
            self.root.after(30)
        self.canvas.delete("merge_pop")

    def draw(self):
        for move in getattr(self.game, 'last_moves', []):
            from_row, from_col, to_row, to_col, value = move
            x0 = from_col * TILE_SIZE + TILE_SIZE // 2
            y0 = from_row * TILE_SIZE + TILE_SIZE // 2 + 50
            x1 = to_col * TILE_SIZE + TILE_SIZE // 2
            y1 = to_row * TILE_SIZE + TILE_SIZE // 2 + 50
            self.animate_tile_move(x0, y0, x1, y1, str(value))
        self.draw_merge_pop_effect(getattr(self.game, "merge_positions", []))
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas_width // 2, 25,
            text=f"Score: {self.game.score}",
            font=SCORE_FONT, fill="white"
        )
        for row in range(self.game.get_grid_height()):
            for col in range(self.game.get_grid_width()):
                value = self.game.get_tile(row, col)
                x0 = col * TILE_SIZE + TILE_PADDING
                y0 = row * TILE_SIZE + TILE_PADDING + 50
                x1 = x0 + TILE_SIZE - TILE_PADDING * 2
                y1 = y0 + TILE_SIZE - TILE_PADDING * 2
                color = TILE_COLORS.get(value, "#3c3a32")
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                if value:
                    self.canvas.create_text((x0 + x1)//2, (y0 + y1)//2,
                                            text=str(value), font=FONT, fill="black")

def run_gui(game):
    TwentyFortyEightGUI(game)
