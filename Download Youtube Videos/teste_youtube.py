import sys
import os
import subprocess
import json
import yt_dlp

app_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg = os.path.join(app_path, 'ffmpeg.exe')

# links = 'https://www.youtube.com/watch?v=30VHcPI6sDs&t=1921s&ab_channel=AurioCorr%C3%A1'
# ydl_opts = {'writesubtitles': True, 'skip-download': True}
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([links])

# yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=oHg5SJYRHA0"
links = 'https://www.youtube.com/watch?v=jku4qn0Mchg&t=122s&ab_channel=AurioCorr%C3%A1'
ydl_opts = {'ignoreerrors': True, 'extract-audio': True, 'audio-format': 'mp3', 'audio-quality' : 0}

audio_name = None
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([links])
    info = ydl.extract_info(links)
    audio_name = info.get('title')

    # info = ydl.extract_info(links, download=False)
    
    # # ℹ️ ydl.sanitize_info makes the info json-serializable
    print(json.dumps(ydl.sanitize_info(info)))
    # print('=================================')
    print(info.title)

#audio_name = 'THE LADIES OF  AVALON - CELTIC MUSIC, ELEVAR VIBRAÇÕES DA EMOÇÃO,  DO AMOR,  DA CURA,  E A HARMONIA. [jku4qn0Mchg].f251.webm'



source = os.path.join(app_path, audio_name)

if os.path.isfile(source.replace(' ', '_')):
    os.remove(source.replace(' ', '_'))

# if ' ' in source:
#     os.rename(source, source.replace(' ', '_'))

audio_name = audio_name.replace(' ', '_')
source = source.replace(' ', '_')

file_without_ext = os.path.splitext(source)[0]

print("source: " + source)
print("final: " + os.path.join(app_path, file_without_ext + '.mp3'))

result = subprocess.run(['ffmpeg.exe', '-y', '-i', source, os.path.join(
    app_path, file_without_ext + '.mp3')], shell=True, check=True)

