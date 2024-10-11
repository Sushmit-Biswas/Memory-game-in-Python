import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from game_logic import MemoryGame
from file_manager import ScoreManager
import time
import pygame
import random

class MemoryGameUI:
    def __init__(self, root):
        # Initialize pygame mixer for sound effects
        pygame.mixer.init()
        self.flip_sound = pygame.mixer.Sound('audio\switch.wav')
        self.match_sound = pygame.mixer.Sound('audio\match.wav')
        self.error_sound = pygame.mixer.Sound('audio\error.mp3')

        # Set volume levels for sound effects
        self.flip_sound.set_volume(0.7)
        self.match_sound.set_volume(0.4)
        self.error_sound.set_volume(0.9)

        # Initialize main window properties
        self.root = root
        self.root.title("Memory Game 🧠")
        self.root.iconbitmap('game.ico')  
        self.root.geometry("800x510")
        
        # Initialize game components
        self.score_manager = ScoreManager()
        self.grid_size = 4
        self.card_size = 100
        self.player_name = None

        # Define color palette for UI elements
        self.colors = {
            'background': '#1A1A2E',
            'card_back': '#16213E',
            'card_front': '#0F3460',
            'text': '#E94560',
            'button': '#533483',
            'button_text': '#E94560'
        }

        # Create the initial game screen
        self.create_initial_screen()

    def create_initial_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame for initial screen
        self.initial_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.initial_frame.pack(fill="both", expand=True)

        # Add game title
        title_label = tk.Label(self.initial_frame, text="Memory Game 🧠", font=("Arial", 26, "bold"), bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(pady=(20, 10))

        # Add game instructions
        instructions = """
        Welcome to Memory Game!

        How to play:
        1. Click on a card to reveal its symbol.
        2. Click on another card to find its match.
        3. If the cards match, they stay face up.
        4. If they don't match, they flip back over.
        5. Remember the positions of the cards and try to match 
            all pairs in the fewest moves possible.

        Good luck and have fun!
        """
        instructions_label = tk.Label(self.initial_frame, text=instructions, font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text'], justify=tk.LEFT, wraplength=500)
        instructions_label.pack(pady=20)

        # Add buttons for starting a new game and viewing history
        new_game_button = tk.Button(self.initial_frame, text="New Game", font=("Arial", 16), bg=self.colors['button'], fg=self.colors['button_text'], command=self.start_new_game)
        new_game_button.pack(pady=10)

        history_button = tk.Button(self.initial_frame, text="View History", font=("Arial", 16), bg=self.colors['button'], fg=self.colors['button_text'], command=self.show_history)
        history_button.pack(pady=10)
        
    def start_new_game(self):
        # Prompt for player name and start a new game
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root)
        if self.player_name:
            self.memory_game = MemoryGame(grid_size=self.grid_size)
            self.start_time = time.time()
            self.create_game_ui()

    def create_game_ui(self):
        # Clear the initial screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create game canvas and moves label
        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.card_size, height=self.grid_size * self.card_size, bg=self.colors['background'])
        self.canvas.pack(pady=20, expand=True)
        self.moves_label = tk.Label(self.root, text="Moves: 0", font=("Arial", 16), bg=self.colors['background'], fg=self.colors['text'])
        self.moves_label.pack(pady=10, expand=True)

        # Bind click event and initialize game state
        self.canvas.bind("<Button-1>", self.on_click)
        self.first_card = None
        self.draw_board()

    def draw_board(self):
        # Get current board state and draw it on the canvas
        board = self.memory_game.get_board()
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.card_size, i * self.card_size
                x2, y2 = x1 + self.card_size, y1 + self.card_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors['card_back'], outline=self.colors['text'])
                if board[i][j] != '':
                    self.canvas.create_text(x1 + 50, y1 + 50, text=board[i][j], font=('Arial', 24), fill=self.colors['text'])

    def on_click(self, event):
        # Handle card click events
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
        # Check if the two flipped cards match
        if self.memory_game.check_match():
            self.match_sound.play()
        else:
            self.error_sound.play()

        self.first_card = None
        self.draw_board()
        self.moves_label.config(text=f"Moves: {self.memory_game.get_moves()}")

        # Check if the game is over
        if self.memory_game.is_game_over():
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            congratulation_messages = [
                f"Congratulations {self.player_name}! You completed the game in {self.memory_game.get_moves()} moves.",
                f"Wow, {self.player_name}! You solved the game in {self.memory_game.get_moves()} moves.",
                f"Great job, {self.player_name}! You finished the game in {self.memory_game.get_moves()} moves.",
                f"Excellent work, {self.player_name}! You completed the game in {self.memory_game.get_moves()} moves.",
                f"Bravo, {self.player_name}! You solved the game in {self.memory_game.get_moves()} moves."
            ]
            random_message = random.choice(congratulation_messages)
            messagebox.showinfo("Game Over", random_message)
            self.score_manager.save_score(self.player_name, self.memory_game.get_moves(), time_taken)
            self.create_initial_screen()

    def show_history(self):
        # Display game history in a new window
        history = self.score_manager.get_scores()
        history_window = tk.Toplevel(self.root)
        history_window.title("Score History")
        history_window.iconbitmap('game.ico') 
        history_window.geometry("800x500")
        history_window.configure(bg=self.colors['background'])

        # Create a frame for the table
        frame = tk.Frame(history_window, bg=self.colors['background'])
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Create the table
        table = ttk.Treeview(frame, columns=("Game", "Player", "Moves", "Time Taken", "Date", "Time"), show="headings")
        table.heading("Game", text="Game")
        table.heading("Player", text="Player")
        table.heading("Moves", text="Moves")
        table.heading("Time Taken", text="Time (sec)")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")

        # Configure column widths
        table.column("Game", width=100, anchor=tk.CENTER)
        table.column("Player", width=150, anchor=tk.CENTER) 
        table.column("Moves", width=100, anchor=tk.CENTER)
        table.column("Time Taken", width=120, anchor=tk.CENTER)
        table.column("Date", width=150, anchor=tk.CENTER)
        table.column("Time", width=120, anchor=tk.CENTER)

        # Insert data into the table
        for score in history:
            table.insert("", "end", values=score)

        table.pack(fill="both", expand=True)

        # Configure colors and fonts for the table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background=self.colors['background'],
                        foreground=self.colors['text'],
                        fieldbackground=self.colors['background'],
                        font=('Arial', 12))
        style.configure("Treeview.Heading", 
                        font=('Arial', 14, 'bold'),
                        background=self.colors['button'],
                        foreground=self.colors['button_text'])

        # Add a title to the history window
        tk.Label(history_window, 
                 text="Game History", 
                 font=("Arial", 20, "bold"), 
                 bg=self.colors['background'], 
                 fg=self.colors['text']).pack(pady=(0, 20), expand=True)
