# main.py
import tkinter as tk
from gui import TextSplitterGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")  # 아이콘 지정
    app = TextSplitterGUI(root)
    root.mainloop()