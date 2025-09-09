import os
from output_dir import output_dir_create
from update_tags_artist_tracktitle import get_deezer_track_info_audio, add_cover_art_audio, update_mp3_tags_audio, rename_file_audio, subtract_string

DEEZER_API_BASE_URL = 'https://api.deezer.com'

def update_tags_for_downloaded_file_all_mp3_audio(output_path):
    # Verifica se há arquivos MP3 no diretório
    mp3_files = [filename for filename in os.listdir(output_path) if filename.endswith('.mp3')]

    if not mp3_files:
        print("\nDiretório não possui arquivos MP3.")
        return
    
    # Atualiza tags para cada arquivo MP3 encontrado
    for filename in mp3_files:
        file_path = os.path.join(output_path, filename)
            
        print(f"\nPara o arquivo {filename}")
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
            print(f"Arquivo renomeado para {subtract_string(new_file_name)}")

def update_tags_all_mp3_audio():
    output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
    update_tags_for_downloaded_file_all_mp3_audio(output_path)

if __name__ == "__main__":
    update_tags_all_mp3_audio()