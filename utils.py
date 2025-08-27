# utils.py
import sys
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def pick_file_gui(title="Select file", filetypes=(("All files", "*.*"),)):
    """Opens a file picker GUI and returns the selected file path (or None)."""
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path if file_path else None

def select_file():
    """
    Returns a valid file path:
    1. From command line arguments if provided.
    2. Otherwise, opens a GUI file picker.
    Exits program if no valid file is selected.
    """
    # Step 1: Check CLI argument
    path = sys.argv[1] if len(sys.argv) > 1 else None

    # Step 2: If no CLI path, open GUI
    if not path:
        path = pick_file_gui()

    # Step 3: Validate path
    if not path or not os.path.exists(path):
        print("No file selected or file does not exist. Exiting.")
        sys.exit()

    return path
