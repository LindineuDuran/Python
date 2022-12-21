import tkinter as tk

root = tk.Tk()
root.title('Tkinter Window Demo')

title = root.title()
print("Título da janela: " + title)
root.geometry('600x400+50+50')

root.mainloop()
