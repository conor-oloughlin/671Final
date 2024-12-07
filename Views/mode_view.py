import tkinter as tk

class ModeView:
    def __init__(self, root):
        """
        Initializes the ModeView to allow the user to select the game mode.

        Preconditions:
        - `root` is a valid Tkinter root or parent window.

        Postconditions:
        - `self.mode` is initialized to None.
        - `self.window` is created as a Toplevel window for mode selection.
        - Two buttons ("Graphical" and "Text") are added to `self.window` for mode selection.
        """
        self.mode = None
        self.window = tk.Toplevel(root)
        self.window.title("Game Mode")

        graphical_button = tk.Button(self.window, text="Graphical", command=lambda: self.set_mode("graphical"))
        text_button = tk.Button(self.window, text="Text", command=lambda: self.set_mode("text"))
        graphical_button.pack(pady=10)
        text_button.pack(pady=10)

    def set_mode(self, mode):
        """
        Sets the game mode and closes the mode selection window.

        Preconditions:
        - `mode` is a string and must be either "graphical" or "text".

        Postconditions:
        - `self.mode` is set to "graphical" or "text" based on the user's choice.
        - `self.window` is destroyed after the mode is set.
        """
        if mode == "graphical":
            self.mode = "graphical"
        elif mode == "text":
            self.mode = "text"
        
        self.window.destroy()