import os
from download_mp3 import download_youtube_audio
from download_playlist_mp3 import download_youtube_playlist_audio
from output_dir import output_dir_create
from update_tags_artist_tracktitle import get_deezer_track_info_audio, update_mp3_tags_audio, add_cover_art_audio, rename_file_audio, subtract_string

DEEZER_API_BASE_URL = 'https://api.deezer.com'

def update_tags_for_downloaded_files(output_path, titles):
    for title in titles:
        file_path = os.path.join(output_path, title)
        
        if not os.path.exists(file_path):
            print(f"\nO arquivo {subtract_string(file_path)} não existe.")
            while not os.path.exists(file_path):
                file_path = input("Por favor, informe o título correto com a extensão .mp3 para o arquivo {title}: ")
                file_path = os.path.join(output_path, file_path)
                if not os.path.exists(file_path):
                    print(f"\nO arquivo {title} ainda não foi encontrado. Tente novamente.")
        
        print(f"\nPara o arquivo {title}:")
        artist = input("Digite o nome do artista: ")
        track_title = input("Digite o título da música: ")
        info = get_deezer_track_info_audio(artist, track_title)

        if info:
            update_mp3_tags_audio(file_path, info)
            add_cover_art_audio(file_path, info.get('cover_url'))
            new_file_name = rename_file_audio(file_path, info.get('artist', ''), info.get('title', ''))
            print(f"Arquivo renomeado para {subtract_string(new_file_name)}")
        else:
            print("Não foi possível obter informações sobre a música.")
            new_file_name = rename_file_audio(file_path, artist, track_title)
            print(f"Arquivo renomeado para {new_file_name}")

def download_youdzer_audio():
    output_path = output_dir_create('mp3') # Diretório onde os arquivos serão salvos e pesquisados
    url = input("\nDigite a URL do vídeo ou playlist do YouTube: ")

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