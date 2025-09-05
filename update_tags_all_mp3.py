import os
from update_tags_artist_tracktitle import get_deezer_track_info_audio, display_info, add_cover_art_audio, update_mp3_tags_audio, rename_file_audio, subtract_string, is_valid_directory
from output_dir import output_dir_create

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

def update_tags_all_mp3_audio():
    choice = input("\nVocê deseja atualizar os metatados de um arquivo MP3 do diretório padrão? (Responda com 's' para sim ou 'n' para são): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        update_tags_for_downloaded_file_all_mp3_audio(output_path)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está os arquivos MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print(f"\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input(f"Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print(f"\nO diretório informado ainda é inválido.")  
        update_tags_for_downloaded_file_all_mp3_audio(output_path)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 10 do menu e tente novamente.")

if __name__ == "__main__":
    update_tags_all_mp3_audio()