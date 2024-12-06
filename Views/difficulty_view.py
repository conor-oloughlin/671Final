# View for initial dialogue box to select difficulty
import tkinter as tk

class DifficultyView:
    def __init__(self):
        self.level = None  # Store the selected difficulty level
        self.rows = 8
        self.cols = 8
        self.mines = 10
        self.treasures = 1
        self.window = tk.Tk()
        self.window.title("Select Difficulty")

        beginner_button = tk.Button(self.window, text="Beginner", command=lambda: self.set_difficulty("beginner"))
        intermediate_button = tk.Button(self.window, text="Intermediate", command=lambda: self.set_difficulty("intermediate"))
        expert_button = tk.Button(self.window, text="Expert", command=lambda: self.set_difficulty("expert"))
        beginner_button.pack(pady=10)
        intermediate_button.pack(pady=10)
        expert_button.pack(pady=10)

        self.window.mainloop()

    def set_difficulty(self, level):
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