import ffmpeg
import os
import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, APIC, TRCK
from mutagen.id3 import ID3NoHeaderError
from io import BytesIO
from PIL import Image
from update_tags_artist_tracktitle import get_deezer_track_info_audio, display_info

def update_mp3_tags_audio_join_mp3(file_path, selected_info):
    try:
        if not os.path.exists(file_path):
            print(f"O arquivo {subtract_string_join_mp3(file_path)} não existe.")
            return

        try:
            audio = ID3(file_path)
        except ID3NoHeaderError:
            audio = ID3()

        # Remove todas as tags existentes antes de adicionar novas
        for tag in list(audio.keys()):
            del audio[tag]

        audio[TPE1] = TPE1(encoding=3, text=selected_info.get('artist', ''))
        audio[TALB] = TALB(encoding=3, text=selected_info.get('album', ''))
        audio[TYER] = TYER(encoding=3, text=selected_info.get('year', ''))
        audio[TCON] = TCON(encoding=3, text=selected_info.get('genre', ''))

        audio.save()
        print(f"Tags ID3 do arquivo {subtract_string_join_mp3(file_path)} atualizadas com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar as tags ID3: {e}")

def add_cover_art_audio_join_mp3(file_path, cover_url):
    if not cover_url:
        print("Nenhuma capa de álbum fornecida.")
        return

    try:
        response = requests.get(cover_url)
        response.raise_for_status()
        cover_image = BytesIO(response.content)
        
        with Image.open(cover_image) as img:
            img.verify()

        try:
            audio = ID3(file_path)
        except ID3NoHeaderError:
            audio = ID3()

        # Remove todas as tags de imagem existentes
        for tag in list(audio.keys()):
            if isinstance(audio[tag], APIC):
                del audio[tag]

        audio[APIC] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=response.content
        )

        audio.save()
        print(f"Capa do álbum adicionada com sucesso para {subtract_string_join_mp3(file_path)}")
    except Exception as e:
        print(f"Erro ao adicionar a capa: {e}")

def subtract_string_join_mp3(file_path):
    home_dir = os.environ['HOME']
    substring_to_remove = f"{home_dir}/youdzer/join_mp3/"
    new_string = file_path.replace(substring_to_remove, "")
    return new_string    

def subtract_string_temp_faded(file_path):
    home_dir = os.environ['HOME']
    substring_to_remove = f"{home_dir}/youdzer/mp3/temp_faded/faded_"
    new_string = file_path.replace(substring_to_remove, "")
    return new_string

def update_tags_for_downloaded_file_artist_tracktitle_audio_album(output_path, file_name_with_extension):
        # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
        # incluindo uma barra no meio das variáveis para acertar o caminho
        file_path = os.path.join(output_path, file_name_with_extension)

        if not os.path.exists(file_path):
            print(f"\nO arquivo {subtract_string_join_mp3(file_path)} não existe.")
            return
        
        print(f"\nPara o arquivo {subtract_string_join_mp3(file_path)}")
        artist = input("Digite o nome do artista: ")
        track_title = input("Digite o título da música: ")
        info = get_deezer_track_info_audio(artist, track_title)

        if info:
            selected_info = display_info(info)
            if selected_info is None:
                print("\nConforme solicitado, o arquivo foi mantido como está.")
                return
            update_mp3_tags_audio_join_mp3(file_path, selected_info)
            add_cover_art_audio_join_mp3(file_path, selected_info.get('cover_url'))
            print(f"Arquivo atualizado com sucesso: {subtract_string_join_mp3(file_path)}")
        else:
            print("Não foi possível obter informações sobre a música.")