from ctypes import windll
import tkinter as tk


root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()
