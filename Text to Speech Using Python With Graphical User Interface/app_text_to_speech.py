import tkinter as tk
from tkinter import ttk
import pyttsx3 as tts

engine = tts.init()

def text_to_speech():
    # voices = engine.getProperty('voice')
    # print(voices)
    # engine.setProperty('voice', voices)
    # engine.setProperty('voice' 'brazil')

    engine.setProperty('rate', 135)

    engine.setProperty('volume', 1)

    t = text.get('0.0', 'end')
    engine.say(t)
    engine.runAndWait()

def save():
    t = text.get('0.0', 'end')
    engine.save_to_file(t, 'test.mp3')
    engine.runAndWait()

root = tk.Tk()
root.title('Text to Speech')

text = tk.Text(font=('Arial', 15))
text.grid(column=0, row=0)

button_frame = tk.Frame()
button_frame.grid(column=0, row=1)

say_btn = ttk.Button(button_frame, text= 'Say', command= text_to_speech)
save_btn = ttk.Button(button_frame, text= 'Save', command= save)

say_btn.grid(column=0, row=0)
save_btn.grid(column=1, row=0)

root.mainloop()