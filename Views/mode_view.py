import tkinter as tk

class ModeView:
    def __init__(self):
        self.mode = None
        self.window = tk.Tk()
        self.window.title("Game Mode")

        graphical_button = tk.Button(self.window, text="Graphical", command=lambda: self.set_mode("graphical"))
        text_button = tk.Button(self.window, text="Text", command=lambda: self.set_mode("text"))
        graphical_button.pack(pady=10)
        text_button.pack(pady=10)

        self.window.mainloop()

    def set_mode(self, mode):
        if mode == "graphical":
            self.mode = "graphical"
        elif mode == "text":
            self.mode = "text"
        self.window.destroy()