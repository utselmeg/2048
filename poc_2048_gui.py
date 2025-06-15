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
        canvas_height = TILE_SIZE * game.get_grid_height() + 50
        canvas_width = TILE_SIZE * game.get_grid_width()
        self.canvas = tk.Canvas(self.root, width=canvas_width,
                                height=canvas_height, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        self.root.bind("<Key>", self.key_handler)
        self.score_text = self.canvas.create_text(
            canvas_width // 2, 25, text="Score: 0",
            font=SCORE_FONT, fill="white"
        )
        self.draw()
        self.root.mainloop()

    def key_handler(self, event):
        direction = {"Up": 1, "Down": 2, "Left": 3, "Right": 4}.get(event.keysym)
        if direction:
            self.game.move(direction)
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.score_text = self.canvas.create_text(
            self.canvas.winfo_width() // 2, 25,
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
