import os
import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TYER, TCON, APIC, TRCK
from mutagen.id3 import ID3NoHeaderError
from io import BytesIO
from PIL import Image
from output_dir import output_dir_create

DEEZER_API_BASE_URL = 'https://api.deezer.com'

def get_deezer_track_info_audio(artist, title):
    search_url = f'{DEEZER_API_BASE_URL}/search'
    params = {'q': f'{artist} {title}', 'limit': 3}
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        print(f"Erro ao buscar faixa: {response.status_code}")
        return {}

    data = response.json()
    info = []

    try:
        for track in data.get('data', []):
            track_id = track['id']
        
            # Buscar detalhes da faixa
            track_detail_url = f'{DEEZER_API_BASE_URL}/track/{track_id}'
            response = requests.get(track_detail_url)

            if response.status_code != 200:
                print(f"Erro ao buscar detalhes da faixa: {response.status_code}")
                return {}

            track_detail = response.json()
            
            # Obter informações detalhadas
            album_id = track_detail['album']['id']
            album = track_detail['album']['title']
            artist = track_detail['artist']['name']
            title = track_detail['title']
            genre = track_detail['album'].get('genre', {}).get('name', '')
            release_date = track_detail['album'].get('release_date', '').split('-')[0]
            cover_url = track_detail['album'].get('cover_xl', '')
            collaborators = [artist['name'] for artist in track_detail.get('contributors', [])]
            contributors = ', '.join(collaborators)
            collaborators_less_main = [
                contributor['name'] for contributor in track_detail.get('contributors', [])
                if contributor['name'] != artist
            ]
            contributors_less_main = ', '.join(collaborators_less_main)

            # Buscar todas as faixas do álbum
            album_tracks_url = f'{DEEZER_API_BASE_URL}/album/{album_id}/tracks'
            response = requests.get(album_tracks_url)

            if response.status_code != 200:
                print(f"Erro ao buscar faixas do álbum: {response.status_code}")
                return {}

            album_tracks = response.json()['data']

            # Encontrar o número da faixa
            track_number = next((i + 1 for i, t in enumerate(album_tracks) if t['id'] == track_id), None)

            info.append({
                'album': album,
                'artist': artist,
                'title': title,
                'genre': genre,
                'year': release_date,
                'cover_url': cover_url,
                'track_number': track_number,
                'album_tracks': album_tracks,
                'contributors': contributors,
                'contributors_less_main': contributors_less_main
            })
        return info
    except (KeyError, IndexError):
        print("Informações não encontradas.")
        return []

def display_info(info):
    print("\nResultados encontrados:")
    for idx, result in enumerate(info):
        print(f"{idx + 1}:")
        print(f"  Artista: {result['artist']}")    
        print(f"  Título: {result['title']}")
        print(f"  Álbum: {result['album']}")
        print(f"  Faixa: {result['track_number']}")
        print(f"  Ano: {result['year']}")
        print(f"  Colaboradores: {result['contributors']}")
        print()

    print("Digite 0 se você deseja manter o arquivo como está.")

    while True:
        try:
            choice = int(input("Escolha o número do resultado que deseja usar: "))
            if choice == 0:
                return None  # Retorna None se o usuário optar por não fazer alterações
            elif 1 <= choice <= len(info):
                return info[choice - 1]
            else:
                print("\nNúmero inválido. Tente novamente.")
        except ValueError:
            print("\nEntrada inválida. Digite um número.")

def update_mp3_tags_audio(file_path, selected_info):
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

        audio[TIT2] = TIT2(encoding=3, text=selected_info.get('title', ''))
        audio[TPE1] = TPE1(encoding=3, text=selected_info.get('artist', ''))
        audio[TALB] = TALB(encoding=3, text=selected_info.get('album', ''))
        audio[TYER] = TYER(encoding=3, text=selected_info.get('year', ''))
        audio[TCON] = TCON(encoding=3, text=selected_info.get('genre', ''))
        audio[TRCK] = TRCK(encoding=3, text=str(selected_info.get('track_number', '')))

        audio.save()
        print(f"Tags ID3 do arquivo {subtract_string(file_path)} atualizadas com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar as tags ID3: {e}")

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

def rename_file_audio(file_path, selected_info):
    try:
        # Extraindo informações do dicionário
        contributors = selected_info.get('contributors', '')
        contributors_less_main = selected_info.get('contributors_less_main', '')
        artist = selected_info.get('artist', '')
        title = selected_info.get('title', '')
        track_number = selected_info.get('track_number', '')
        album_tracks = selected_info.get('album_tracks', '')

        # Transformando a lista de contribuidores em uma lista
        contributors = contributors.split(', ')

        if len(album_tracks) > 1 and len(contributors) > 1:
            # Cria o novo nome do arquivo com base no número da faixa, nome do artista, título da música e colaboradores
            new_file_name = f"{track_number}. {artist} - {title} feat. {contributors_less_main}.mp3"
        elif len(album_tracks) == 1 and len(contributors) > 1:
            # Cria o novo nome do arquivo com base no  nome do artista, título da música e colaboradores
            new_file_name = f"{artist} - {title} feat. {contributors_less_main}.mp3"
        elif len(album_tracks) > 1 and len(contributors) == 1:
            # Cria o novo nome do arquivo com base no número da faixa, nome do artista e título da música
            new_file_name = f"{track_number}. {artist} - {title}.mp3"
        else:
            # O else cobre o caso em que tanto album_tracks quanto contributors são == 1 (len(album_tracks) == 1 and len(contributors) == 1)
            # Cria o novo nome do arquivo com base no artista e no título
            new_file_name = f"{artist} - {title}.mp3"

        dir_name = os.path.dirname(file_path)
        new_file_path = os.path.join(dir_name, new_file_name)
        # Renomeia o arquivo original para o novo nome
        os.rename(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        print(f"Erro ao renomear o arquivo MP3: {e}")

def subtract_string(file_path):
    home_dir = os.environ['HOME']
    substring_to_remove = f"{home_dir}/youdzer/mp3/"
    new_string = file_path.replace(substring_to_remove, "")
    return new_string
    
def is_valid_directory(path):
    return os.path.isdir(path)

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
            selected_info = display_info(info)
            if selected_info is None:
                print("\nConforme solicitado, o arquivo foi mantido como está.")
                return
            update_mp3_tags_audio(file_path, selected_info)
            add_cover_art_audio(file_path, selected_info.get('cover_url'))
            new_file_name = rename_file_audio(file_path, selected_info)
            if new_file_name:
                print(f"Arquivo renomeado para {subtract_string(new_file_name)}")
        else:
            print("Não foi possível obter informações sobre a música.")

def update_tags_artist_tracktitle_audio():
    choice = input("\nVocê deseja atualizar os metatados de um arquivo MP3 do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp3: ")
        update_tags_for_downloaded_file_artist_tracktitle_audio(output_path, file_name_with_extension)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está o arquivo MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")  
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp3: ")
        update_tags_for_downloaded_file_artist_tracktitle_audio(output_path, file_name_with_extension)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 9 do menu e tente novamente.")

if __name__ == "__main__":
    update_tags_artist_tracktitle_audio()