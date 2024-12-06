import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time

import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

class TestingView:
    def __init__(self):
        self.is_testing = messagebox.askyesno("Testing Mode", "Enter testing mode?")

    def uploadCSV(self):
        temp_root = tk.Tk()
        temp_root.withdraw()
        # Opens a dialogue to select a csv file from the user's file directory
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], parent=temp_root)
        if file_path:
            print(f"Selected file: {file_path}")
            return file_path
        else:
            messagebox.showerror("Invalid Board", "The test board is not valid.")
        # Destroys the tkinter window
        temp_root.destroy()