from pytube import YouTube
import subprocess
import os

app_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg = os.path.join(app_path, 'ffmpeg-2022-12-21-git-eef763c705-full_build', 'bin', 'ffmpeg.exe')

path = 'D:\\Músicas\\'

video_url = input("Please enter the video URL: ")
yt = YouTube(video_url)

audio = yt.streams.get_audio_only()
audio.download(output_path=path)

file_name = audio.default_filename

source = path + file_name

if ' ' in file_name:
     os.rename(source, source.replace(' ', '_'))
     file_name = source.replace(' ','_')

file_without_ext = os.path.splitext(file_name)[0]

subprocess.Popen([ffmpeg, '-i', file_name, file_without_ext + '.mp3'])
os.remove(file_name.replaca('/',''))
