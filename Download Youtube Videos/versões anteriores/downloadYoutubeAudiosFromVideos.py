import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from pytube import YouTube
import shutil, os

def download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.filter(only_audio=True).first()

    try:
        out_file_name = youtubeObject.default_filename
        out_file = youtubeObject.download()
    except:
        print("There has been an error in downloading your youtube video")

    print("This download has completed! Yahoooo!")
    return out_file_name

def save_mp3(out_file):
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def move_video(video_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)
    #print(video_name)
    shutil.move(dir_path + '\\' + video_name, target.get())

def download_clicked():
    """ callback when the download button clicked
    """
    msg = f'You entered url link: {link.get()}'
    showinfo( title='Information', message=msg)
    out_file = download(link.get())
    new_file = save_mp3(out_file)
    move_video(new_file)

    msg = f'This download has completed! Yahoooo!: {new_file}'
    showinfo( title='Information', message=msg)

# root window
root = tk.Tk()
root.geometry("500x150")
root.resizable(False, False)
root.title('Downloading YouTube video')

# store url link and target folder
link = tk.StringVar()
target = tk.StringVar()
video_name = ''

#link = input("Put your youtube link here!!! URL: ")

# Download in frame
frm_download = ttk.Frame(root)
frm_download.pack(padx=10, pady=10, fill='x', expand=True)

# link
link_label = ttk.Label(frm_download, text="URL link:")
link_label.pack(fill='x', expand=True)

link_entry = ttk.Entry(frm_download, textvariable=link)
link_entry.pack(fill='x', expand=True)
link_entry.focus()

# target folder
target_label = ttk.Label(frm_download, text="Target:")
target_label.pack(fill='x', expand=True)

target_entry = ttk.Entry(frm_download, textvariable=target)
target_entry.pack(fill='x', expand=True)

# download button
download_button = ttk.Button(frm_download, text="Download", command=download_clicked)
download_button.pack(fill='x', expand=True, pady=10)

root.mainloop()
