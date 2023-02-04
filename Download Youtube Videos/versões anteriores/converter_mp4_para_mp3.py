import subprocess
import os
from pytube import YouTube

app_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg = os.path.join(
    app_path, 'ffmpeg-2022-12-21-git-eef763c705-full_build', 'bin', 'ffmpeg.exe')

file_name = 'MúsicaXamãnica.mp4'
# source = path + file_name

file_without_ext = os.path.splitext(file_name)[0]

subprocess.Popen([ffmpeg, '-i', 'D:\\Músicas\\'+file_name,
                 'D:\\Músicas\\'+file_without_ext + '.mp3'])
# os.remove(file_name.replaca('/',''))
