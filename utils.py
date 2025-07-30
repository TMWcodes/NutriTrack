# utils.py
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def pick_file_gui(title="Select file", filetypes=(("All files", "*.*"),)):
    """Opens a file picker and returns the selected file path."""
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path