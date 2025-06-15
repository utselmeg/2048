import tkinter as tk

TILE_SIZE = 100
TILE_PADDING = 3
FONT = ("Verdana", 24, "bold")
SCORE_FONT = ("Verdana", 16, "bold")
BACKGROUND_COLOR = "#bbada0"
BUTTON_COLOR = "#f46636"
TEXT_COLOR = "#f9f6f2"
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
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        self.canvas_width = TILE_SIZE * game.get_grid_width()
        self.canvas_height = TILE_SIZE * game.get_grid_height()
        self.container = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.container.pack(padx=10, pady=0)
        # Top bar
        self.top_bar = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        self.top_bar.pack(fill="x", pady=(10, 5), padx=10)

        self.score_label = tk.Label(self.top_bar, text=f"Score: {self.game.score}",
                                    font=SCORE_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        self.score_label.pack(side="left")

        self.restart_button = tk.Canvas(self.top_bar, width=80, height=28,
                                        bg=BACKGROUND_COLOR, highlightthickness=0)
        self.restart_button.pack(side="right")

        def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
            points = [x1 + radius, y1,x1 + radius, y1,x2 - radius, y1,x2 - radius, y1,x2, y1,
                      x2, y1 + radius,x2, y1 + radius,x2, y2 - radius,x2, y2 - radius,x2, y2,
                      x2 - radius, y2,x2 - radius, y2,x1 + radius, y2,x1 + radius, y2,x1, y2,
                      x1, y2 - radius,x1, y2 - radius,x1, y1 + radius,x1, y1 + radius,x1, y1]
            return self.restart_button.create_polygon(points, **kwargs, smooth=True)

        round_rectangle(0, 0, 80, 28, radius=20, fill=BUTTON_COLOR, outline=BUTTON_COLOR, width=0)
        # self.restart_button.create_rectangle(0, 0, 80, 28, fill=BUTTON_COLOR,
        #                                      outline=BUTTON_COLOR, width=0)
        self.restart_button.create_text(40, 14, text="Restart", fill=TEXT_COLOR,
                                        font=("Verdana", 12, "bold"))
        self.restart_button.bind("<Button-1>", lambda e: self.restart_game())

        # Canvas for game grid
        self.canvas = tk.Canvas(self.container, width=self.canvas_width,
                                height=self.canvas_height, bg=BACKGROUND_COLOR,
                                highlightthickness=0)
        self.canvas.pack(pady=(0, 10))

        self.root.bind("<Key>", self.key_handler)
        self.draw()
        self.root.mainloop()

    def restart_game(self):
        self.game.reset()
        self.draw()

    def key_handler(self, event):
        if not self.is_game_over():
            direction = {"Up": 1, "Down": 2, "Left": 3, "Right": 4}.get(event.keysym)
            if direction:
                self.game.move(direction)
                self.draw()

    def is_game_over(self):
        for direction in [1, 2, 3, 4]:
            backup_grid = [row[:] for row in self.game._grid]
            backup_score = self.game.score
            self.game.move(direction)
            if self.game._grid != backup_grid:
                self.game._grid = backup_grid
                self.game.score = backup_score
                return False
        return True

    def draw_merge_pop_effect(self, merged_tiles):
        # merged_tiles = list of (row, col, value)
        size_steps = [1.1, 1.3, 1.1, 1.0]
        for scale in size_steps:
            self.canvas.delete("merge_pop")
            for row, col, value in merged_tiles:
                x = col * TILE_SIZE + TILE_SIZE // 2
                y = row * TILE_SIZE + TILE_SIZE // 2
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
            y0 = from_row * TILE_SIZE + TILE_SIZE // 2
            x1 = to_col * TILE_SIZE + TILE_SIZE // 2
            y1 = to_row * TILE_SIZE + TILE_SIZE // 2
            self.animate_tile_move(x0, y0, x1, y1, str(value))
        self.draw_merge_pop_effect(getattr(self.game, "merge_positions", []))
        self.canvas.delete("all")
        self.score_label.config(
            text=f"Score: {self.game.score}"
        )
        for row in range(self.game.get_grid_height()):
            for col in range(self.game.get_grid_width()):
                value = self.game.get_tile(row, col)
                x0 = col * TILE_SIZE + TILE_PADDING
                y0 = row * TILE_SIZE + TILE_PADDING
                x1 = x0 + TILE_SIZE - TILE_PADDING * 2
                y1 = y0 + TILE_SIZE - TILE_PADDING * 2
                color = TILE_COLORS.get(value, "#3c3a32")
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                if value:
                    self.canvas.create_text((x0 + x1)//2, (y0 + y1)//2,
                                            text=str(value), font=FONT, fill="black")
        if self.is_game_over():
            self.canvas.create_text(
                self.canvas_width // 2,
                self.canvas_height // 2,
                text="Game Over!",
                font=("Verdana", 32, "bold"),
                fill="red"
            )
    def animate_tile_move(self, x0, y0, x1, y1, text, steps=5):
        tile = self.canvas.create_text(x0, y0, text=text, font=FONT, fill="black")
        dx = (x1 - x0) / steps
        dy = (y1 - y0) / steps
        for _ in range(steps):
            self.canvas.move(tile, dx, dy)
            self.root.update()
            self.root.after(10)
        self.canvas.delete(tile)

def run_gui(game):
    TwentyFortyEightGUI(game)
