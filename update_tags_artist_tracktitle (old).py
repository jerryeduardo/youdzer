import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, APIC
from mutagen.id3 import ID3NoHeaderError
import os
from io import BytesIO
from PIL import Image
from output_dir import output_dir_create

DEEZER_API_BASE_URL = 'https://api.deezer.com'

def get_deezer_track_info_audio(artist, title):
    search_url = f'{DEEZER_API_BASE_URL}/search'
    params = {'q': f'{artist} {title}', 'limit': 1}
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        print(f"Erro ao buscar faixa: {response.status_code}")
        return {}

    data = response.json()

    try:
        track = data['data'][0]
        track_id = track['id']
        
        # Buscar detalhes da faixa
        track_detail_url = f'{DEEZER_API_BASE_URL}/track/{track_id}'
        response = requests.get(track_detail_url)

        if response.status_code != 200:
            print(f"Erro ao buscar detalhes da faixa: {response.status_code}")
            return {}

        track_detail = response.json()
        
        # Obter informações detalhadas
        album = track_detail['album']['title']
        genre = track_detail['album'].get('genre', {}).get('name', '')
        release_date = track_detail['album'].get('release_date', '').split('-')[0]
        cover_url = track_detail['album'].get('cover_xl', '')

        return {
            'album': album,
            'artist': track_detail['artist']['name'],
            'title': track_detail['title'],
            'genre': genre,
            'year': release_date,
            'cover_url': cover_url
        }
    except (KeyError, IndexError):
        print("Informações não encontradas.")
        return {}

def add_cover_art_audio(file_path, cover_url):
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
        print(f"Capa do álbum adicionada com sucesso para {subtract_string(file_path)}")
    except Exception as e:
        print(f"Erro ao adicionar a capa: {e}")

def update_mp3_tags_audio(file_path, info):
    try:
        if not os.path.exists(file_path):
            print(f"O arquivo {subtract_string(file_path)} não existe.")
            return

        try:
            audio = ID3(file_path)
        except ID3NoHeaderError:
            audio = ID3()

        # Remove todas as tags existentes antes de adicionar novas
        for tag in list(audio.keys()):
            del audio[tag]

        audio[TIT2] = TIT2(encoding=3, text=info.get('title', ''))
        audio[TPE1] = TPE1(encoding=3, text=info.get('artist', ''))
        audio[TALB] = TALB(encoding=3, text=info.get('album', ''))
        audio[TYER] = TYER(encoding=3, text=info.get('year', ''))
        audio[TCON] = TCON(encoding=3, text=info.get('genre', ''))

        audio.save()
        print(f"Tags ID3 do arquivo {subtract_string(file_path)} atualizadas com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar as tags ID3: {e}")

def rename_file_audio(file_path, artist, title):
    # Cria o novo nome do arquivo com base no artista e no título
    new_file_name = f"{artist} - {title}.mp3"
    dir_name = os.path.dirname(file_path)
    new_file_path = os.path.join(dir_name, new_file_name)
    # Renomeia o arquivo original para o novo nome
    os.rename(file_path, new_file_path)
    return new_file_path

def subtract_string(file_path):
    home_dir = os.environ['HOME']
    substring_to_remove = f"{home_dir}youdzer/mp3/"
    new_string = file_path.replace(substring_to_remove, "")
    return new_string
    
def update_tags_for_downloaded_file_artist_tracktitle_audio(output_path, file_name_with_extension):
        # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
        # incluindo uma barra no meio das variáveis para acertar o caminho
        file_path = os.path.join(output_path, file_name_with_extension)

        if not os.path.exists(file_path):
            print(f"\nO arquivo {subtract_string(file_path)} não existe.")
            return
        
        print(f"\nPara o arquivo {subtract_string(file_path)}")
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

def update_tags_artist_tracktitle_audio():
    output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
    file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp3: ")
    update_tags_for_downloaded_file_artist_tracktitle_audio(output_path, file_name_with_extension)

if __name__ == "__main__":
    update_tags_artist_tracktitle_audio()