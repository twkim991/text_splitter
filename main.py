# main.py
import tkinter as tk
from gui import TextSplitterGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSplitterGUI(root)
    root.mainloop()