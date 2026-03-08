import yt_dlp
"""
o yt-dlp precisa do FFmpeg para processar o vídeo/áudio após o download, e ele deve estar instalado e no PATH.
Instalar via winget (mais rápido): winget install ffmpeg
"""

def baixar(url, opcao):
    """Ler o doc 'Usar Cookie Exporter.odt' para baixar o cookies.txt (NÃO SUBIR O ARQUIVO PARA O GITHUB)"""
    """Execute o seguinte comando para baixar os cookies: yt-dlp --cookies-from-browser chrome --cookies cookies.txt """
    base_opts = {
        "cookiefile": "D:\Desenvolvimento de Sistemas\cookies.txt",       # <— cookies obrigatórios
        "check_formats": True,
        "retries": 10,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "outtmpl": "%(title)s.%(ext)s",
    }

    if opcao == "1":
        print("\n🟦 Baixando VÍDEO na melhor qualidade sem DRM...\n")
        ydl_opts = {
            "format": "bv*+ba/b",
            "check_formats": True,
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
            "retries": 10,
            "http_headers": {"User-Agent": "Mozilla/5.0"},
        }

    elif opcao == "2":
        print("\n🟩 Baixando ÁUDIO em M4A (melhor qualidade)...\n")
        ydl_opts = {
            "format": "bestaudio/best",
            "check_formats": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                }
            ],
            "outtmpl": "%(title)s.%(ext)s",
        }

    elif opcao == "3":
        print("\n🟧 Baixando ÁUDIO em MP3...\n")
        ydl_opts = {
            "format": "bestaudio/best",
            "check_formats": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "%(title)s.%(ext)s",
        }

    else:
        print("❌ Opção inválida.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    """
    Escolha     Ação                                                Output
    1           Baixa vídeo + áudio na melhor qualidade não-DRM     .mp4
    2           Baixa apenas áudio na melhor qualidade              .m4a
    3           Baixa áudio convertido para MP3                     .mp3
    """
    print("=== MENU DE DOWNLOAD ===")
    print("1 - Baixar VÍDEO")
    print("2 - Baixar ÁUDIO (M4A)")
    print("3 - Baixar ÁUDIO (MP3)")

    escolha = input("Escolha uma opção: ").strip()

    link = input("URL do vídeo: ").strip()

    baixar(link, escolha)
