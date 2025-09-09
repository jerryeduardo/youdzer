import ffmpeg
import os
from mutagen.mp3 import MP3
from output_dir import output_dir_create
from update_tags_artist_tracktitle import is_valid_directory
from update_tags_artist_tracktitle_album import update_tags_for_downloaded_file_artist_tracktitle_audio_album, subtract_string_join_mp3, subtract_string_temp_faded

def joinup_all_mp3(output_path):
    # Verifica se há arquivos MP3 no diretório
    mp3_files = [filename for filename in os.listdir(output_path) if filename.endswith('.mp3')]

    if not mp3_files:
        print("\nDiretório não possui arquivos MP3.")
        return
    
    # Ordena os arquivos por ordem alfabética
    mp3_files.sort()

    # Define o título do arquivo final
    name_final = input("\nDigite um título para o arquivo MP3 após a junção: ")
    print("")

    # Cria pasta e define caminho do arquivo final
    output_join = output_dir_create('join_mp3')
    output_file = os.path.join(output_join, name_final + ".mp3")

    # Cria pasta temporária para arquivos com fade
    temp_faded = output_dir_create('mp3/temp_faded')

    # Aplica fade em cada faixa
    faded_files = []
    total = len(mp3_files)
    print("Iniciando a aplicação de fade in e out nas músicas para a junção")
    for i, filename in enumerate(mp3_files):
        input_path = os.path.join(output_path, filename)
        faded_path = os.path.join(temp_faded, f"faded_{filename}")
        if not os.path.exists(faded_path):
            apply_fade_effects(input_path, faded_path)
            print(f"Fade aplicado na faixa: {filename}\n")
        else:
            if i == total - 1 and all(os.path.exists(os.path.join(temp_faded, f"faded_{f}")) for f in mp3_files):
                print(f"Fade já existente para a faixa: {filename}, pulando...\n")
            else:
                print(f"Fade já existente para a faixa: {filename}, pulando...")
        faded_files.append(faded_path)
    
    # Cria lista de concatenação
    concat_list_path = os.path.join(temp_faded, name_final + ".txt")
    print("Iniciando a listagem das músicas já com fade in e out aplicado para a junção")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for file_path in faded_files:
            f.write(f"file '{file_path}'\n")
            print(f"Adicionando faixa: {subtract_string_temp_faded(file_path)}")

    # Extração de caminho do arquivo de audio MP3 após a junção
    output_folder = os.path.dirname(output_file)

    # Executa FFmpeg para juntar os arquivos
    try:
        print("")
        ffmpeg.input(concat_list_path, format='concat', safe=0).output(output_file, 
            acodec='libmp3lame', 
            audio_bitrate='192k', 
            ar=44100).run()
        print("\nJunção dos arquivos de áudio MP3 realizada e salva com sucesso.")
        print(f"Título do arquivo de áudio MP3 após a junção: {subtract_string_join_mp3(output_file)}")
        print(f"Caminho onde está o arquivo de áudio MP3: {output_folder}")
    except Exception as e:
        print(f"\nErro ao juntar os arquivos MP3: {e}")

    choice = input("\nVocê deseja atualizar os metatados do álbum com base no Deezer no arquivo MP3? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        update_tags_for_downloaded_file_artist_tracktitle_audio_album(output_join, name_final + ".mp3")
    elif choice == 'n':
        return
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 14 do menu e tente novamente.")

def apply_fade_effects(input_path, output_path, fade_in=2, fade_out=2):
    try:
        audio = MP3(input_path)
        duration = audio.info.length
        fade_out_start = max(0, duration - fade_out)

        ffmpeg.input(input_path).output(
            output_path,
            af=f"afade=t=in:st=0:d={fade_in},afade=t=out:st={fade_out_start}:d={fade_out}"
        ).run()
    except Exception as e:
        print(f"Erro ao aplicar fade em {input_path}: {e}")

def join_all_audio():
    choice = input("\nVocê deseja juntar os arquivos de música MP3 do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        joinup_all_mp3(output_path)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está os arquivos MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")  
        joinup_all_mp3(output_path)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 12 do menu e tente novamente.")

if __name__ == "__main__":
    join_all_audio()