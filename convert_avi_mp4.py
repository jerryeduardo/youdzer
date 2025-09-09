import ffmpeg
import os
from output_dir import output_dir_create
from update_tags_artist_tracktitle import is_valid_directory

def converter_avi_mp4(output_path, file_name_with_extension):
    # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
    # incluindo uma barra no meio das variáveis para acertar o caminho
    file_path = os.path.join(output_path, file_name_with_extension)
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    output_mp4 = os.path.join(output_dir_create('mp4'), file_name_without_extension + ".mp4")
    output_folder = os.path.dirname(output_mp4)

    try:
        print(f"")
        ffmpeg.input(file_path).output(output_mp4, 
            s="1920x1080", 
            r=30, 
            video_bitrate='8000k', 
            audio_bitrate='256k', 
            vcodec='libx264', 
            acodec='aac', 
            crf=18, 
            preset='medium', 
            pix_fmt='yuv420p').run()
        print("\nVídeo convertido e salvo com sucesso.")
        print(f"Título do arquivo de vídeo AVI após a conversão para MP4: {file_name_without_extension}")
        print(f"Caminho onde está o arquivo de vídeo convertido para MP4: {output_folder}")
    except Exception as e:
        print(f"Erro ao executar o ffmpeg: {e}")

def convert_video():
    choice = input("\nVocê deseja converter um arquivo de vídeo AVI do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('avi') # Diretório onde os arquivos serão pesquisados
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .avi: ")
        converter_avi_mp4(output_path, file_name_with_extension)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está o arquivo de vídeo AVI (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")  
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .avi: ")
        converter_avi_mp4(output_path, file_name_with_extension)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 10 do menu e tente novamente.")

if __name__ == "__main__":
    convert_video()