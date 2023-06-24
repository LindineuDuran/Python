import os
import subprocess
import yt_dlp

app_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg = os.path.join(app_path, 'ffmpeg.exe')

# yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=oHg5SJYRHA0"
links = 'https://www.youtube.com/watch?v=XKZw2UtWPqA&ab_channel=AurioCorr%C3%A1'
ydl_opts = {'ignoreerrors': True, 'extract-audio': True, 'audio-format': 'mp3', 'audio-quality' : 0}

audio_name = None
id = None
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([links])
    info = ydl.extract_info(links)
    audio_name = info.get('title')
    id = info.get('id')

source = os.path.join(app_path, audio_name + ' [' + id + ']' +'.webm')

if os.path.isfile(source.replace(' ', '_')):
    os.remove(source.replace(' ', '_'))

if ' ' in source:
    os.rename(source, source.replace(' ', '_'))

audio_name = audio_name.replace(' ', '_')
source = source.replace(' ', '_')

file_without_ext = os.path.splitext(source)[0]

result = subprocess.run(['ffmpeg.exe', '-y', '-i', source, os.path.join(app_path, file_without_ext + '.mp3')], shell=True, check=True)
