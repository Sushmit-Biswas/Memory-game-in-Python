import tkinter as tk
from tkinter import messagebox
from game_logic import MemoryGame
from file_manager import ScoreManager
import time
import pygame

class MemoryGameUI:
    def __init__(self, root):
        pygame.mixer.init()
        self.flip_sound = pygame.mixer.Sound('flip.wav')
        self.match_sound = pygame.mixer.Sound('match.wav')
        self.error_sound = pygame.mixer.Sound('error.mp3')

        self.flip_sound.set_volume(0.8)  # Set volume to 80%
        self.match_sound.set_volume(0.5)  # Set volume to 50%
        self.error_sound.set_volume(0.9)  # Set volume to 90%

        
        self.root = root
        self.root.title("Memory Game")
        self.memory_game = MemoryGame(grid_size=4)  # Change grid size to 4x4
        self.score_manager = ScoreManager()
        self.grid_size = 4
        self.card_size = 100
        self.start_time = time.time()

        self.canvas = tk.Canvas(root, width=self.grid_size * self.card_size, height=self.grid_size * self.card_size, bg="black")
        self.canvas.pack()
        self.moves_label = tk.Label(root, text="Moves: 0", font=("Arial", 16), bg="black", fg="white")
        self.moves_label.pack()
        self.history_button = tk.Button(root, text="View History", command=self.show_history, font=("Arial", 12), bg="black", fg="white")
        self.history_button.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.first_card = None
        self.draw_board()

    def draw_board(self):
        board = self.memory_game.get_board()
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.card_size, i * self.card_size
                x2, y2 = x1 + self.card_size, y1 + self.card_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                if board[i][j] != '':
                    self.canvas.create_text(x1 + 50, y1 + 50, text=board[i][j], font=('Arial', 24), fill="white")

    def on_click(self, event):
        x, y = event.x // self.card_size, event.y // self.card_size
        if self.first_card is None:
            if self.memory_game.flip_card(y, x):
                self.flip_sound.play()
                self.first_card = (x, y)
                self.draw_board()
        else:
            if self.memory_game.flip_card(y, x):
                self.flip_sound.play()
                self.draw_board()
                self.root.after(500, self.check_match, x, y)

    def check_match(self, x, y):
        if self.memory_game.check_match():
            self.match_sound.play()
        else:
            self.error_sound.play()

        self.first_card = None
        self.draw_board()
        self.moves_label.config(text=f"Moves: {self.memory_game.get_moves()}")

        if self.memory_game.is_game_over():
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            messagebox.showinfo("Game Over", f"Congratulations! You completed the game in {self.memory_game.get_moves()} moves.")
            self.score_manager.save_score(self.memory_game.get_moves(), time_taken)
            self.root.quit()

    def show_history(self):
        history = self.score_manager.get_scores()
        history_window = tk.Toplevel(self.root)
        history_window.title("Score History")
        tk.Label(history_window, text="Game History", font=("Arial", 16)).pack()
        for score in history:
            tk.Label(history_window, text=f"Game {score[0]} - Moves: {score[1]}, Time: {score[2]} sec on {score[3]} at {score[4]}", font=("Arial", 12)).pack()

    def resize_canvas(self, event):
        self.card_size = min(self.root.winfo_width() // 4, self.root.winfo_height() // 4)
        self.canvas.config(width=self.grid_size * self.card_size, height=self.grid_size * self.card_size)
        self.draw_board()
