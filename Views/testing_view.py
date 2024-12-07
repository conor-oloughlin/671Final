import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time

import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

class TestingView:
    def __init__(self, root):
        """
        Initializes the TestingView to determine if the user wants to enter testing mode.

        Preconditions:
        - `root` is a valid Tkinter root or parent window.

        Postconditions:
        - `self.is_testing` is set to True if the user selects "Yes" in the message box, otherwise False.
        """
        self.is_testing = messagebox.askyesno("Testing Mode", "Enter testing mode?", parent=root)

    def uploadCSV(self, root):
        """
        Prompts the user to select a CSV file for the test board.

        Preconditions:
        - `root` is a valid Tkinter root or parent window.

        Postconditions:
        - Returns the file path to the selected CSV file if the user selects a file.
        - Displays an error message and returns None if no file is selected.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], parent=root)
        if file_path:
            return file_path
        else:
            messagebox.showerror("Invalid Board", "The test board is not valid.", parent=root)
            return None