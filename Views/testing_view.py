import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time

import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

class TestingView:
    def __init__(self, root):
        print("Constructing TestingView")
        self.is_testing = messagebox.askyesno("Testing Mode", "Enter testing mode?", parent=root)

    def uploadCSV(self, root):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], parent=root)
        if file_path:
            print(f"Selected file: {file_path}")
            return file_path
        else:
            messagebox.showerror("Invalid Board", "The test board is not valid.", parent=root)
            return None