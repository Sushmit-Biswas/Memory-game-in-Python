# Python Memory Game using Tkinter and Pygame.
# Developed by: Sushmit Biswas

import tkinter as tk
from ui import MemoryGameUI

def main():
    root = tk.Tk()
    game_ui = MemoryGameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
