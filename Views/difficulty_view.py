# View for initial dialogue box to select difficulty
from tkinter import filedialog, simpledialog
import tkinter as tk

class DifficultyView:
    def __init__(self, root):
        """
        Initializes the DifficultyView to allow the user to select a difficulty level.

        Preconditions:
        - `root` is a valid Tkinter root or parent window.

        Postconditions:
        - `self.level` is initialized to None.
        - `self.rows`, `self.cols`, `self.mines`, and `self.treasures` are initialized to beginner-level defaults.
        - `self.window` is created as a Toplevel window for difficulty selection.
        - Three buttons ("Beginner", "Intermediate", and "Expert") are added to `self.window` for difficulty selection.
        """
        self.level = None
        self.rows = 8
        self.cols = 8
        self.mines = 10
        self.treasures = 1
        self.window = tk.Toplevel(root)
        self.window.title("Select Difficulty")

        beginner_button = tk.Button(self.window, text="Beginner", command=lambda: self.set_difficulty("beginner"))
        intermediate_button = tk.Button(self.window, text="Intermediate", command=lambda: self.set_difficulty("intermediate"))
        expert_button = tk.Button(self.window, text="Expert", command=lambda: self.set_difficulty("expert"))
        beginner_button.pack(pady=10)
        intermediate_button.pack(pady=10)
        expert_button.pack(pady=10)

    def set_difficulty(self, level):
        """
        Sets the difficulty level and updates game parameters accordingly.

        Preconditions:
        - `level` is a string and must be one of: "beginner", "intermediate", "expert".

        Postconditions:
        - `self.level` is set to the selected difficulty level.
        - If "beginner" is selected, the board is set to 8x8 with 10 mines and 1 treasure.
        - If "intermediate" is selected, the board is set to 16x16 with 40 mines and 3 treasures.
        - If "expert" is selected, the board is set to 30x16 with 99 mines and 5 treasures.
        - `self.window` is destroyed after the difficulty is set.
        """
        self.level = level
        if level == "intermediate":
            self.rows = 16
            self.cols = 16
            self.mines = 40
            self.treasures = 3
        elif level == "expert":
            self.rows = 30
            self.cols = 16
            self.mines = 99
            self.treasures = 5
        else:
            # Default to beginner
            self.rows = 8
            self.cols = 8
            self.mines = 10
            self.treasures = 1

        self.window.destroy()