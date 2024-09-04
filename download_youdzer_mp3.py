import yt_dlp
import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, APIC
from mutagen.id3 import ID3NoHeaderError
import os
from io import BytesIO
from PIL import Image
from download_mp3 import download_youtube_audio
from download_playlist_mp3 import download_youtube_playlist_audio
from update_tags_artist_tracktitle import get_deezer_track_info_audio, add_cover_art_audio, update_mp3_tags_audio, rename_file_audio

DEEZER_API_BASE_URL = 'https://api.deezer.com'

def update_tags_for_downloaded_files(output_path, titles):
    for title in titles:
        file_path = os.path.join(output_path, title)
        
        if not os.path.exists(file_path):
            print(f"\nO arquivo {file_path} não existe.")
            while not os.path.exists(file_path):
                file_path = input(f"Por favor, forneça o caminho correto para o arquivo {title}: ")
                if not os.path.exists(file_path):
                    print(f"O arquivo {file_path} ainda não foi encontrado. Tente novamente.")
        
        print(f"\nPara o arquivo {title}:")
        artist = input("Digite o nome do artista: ")
        track_title = input("Digite o título da música: ")

        info = get_deezer_track_info_audio(artist, track_title)

        if info:
            update_mp3_tags_audio(file_path, info)
            add_cover_art_audio(file_path, info.get('cover_url'))
            new_file_name = rename_file_audio(file_path, info.get('artist', ''), info.get('title', ''))
            print(f"Arquivo renomeado para {new_file_name}")
        else:
            print("Não foi possível obter informações sobre a música.")
            new_file_name = rename_file_audio(file_path, artist, track_title)
            print(f"Arquivo renomeado para {new_file_name}")

def download_youdzer_audio():
    url = input("\nDigite a URL do vídeo ou playlist do YouTube: ")
    output_path = '.'  # Diretório onde os arquivos serão salvos e pesquisados

    # Cria o diretório se não existir
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Verifica se a URL fornecida é uma playlist ou um vídeo individual
    if 'list' in url:  # Identifica URL de playlist
        titles = download_youtube_playlist_audio(url, output_path)
    else:
        file_name = download_youtube_audio(url, output_path)
        titles = [file_name] if file_name else []

    if titles:
        update_tags_for_downloaded_files(output_path, titles)

if __name__ == "__main__":
    download_youdzer_audio()