# View for initial dialogue box to select difficulty
from tkinter import simpledialog

class DifficultyView:
    def __init__(self):
        self.level = simpledialog.askstring("Select Level", "Enter Difficulty (beginner, intermediate, expert):", parent=None)