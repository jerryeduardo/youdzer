import ffmpeg
import os
from update_tags_artist_tracktitle import is_valid_directory
from output_dir import output_dir_create

def converter_all_avi_mp4(output_path):
    # Verifica se há arquivos AVI no diretório
    avi_files = [filename for filename in os.listdir(output_path) if filename.endswith('.avi')]

    if not avi_files:
        print("\nDiretório não possui arquivos AVI.")
        return
    
    # Ordenar os arquivos por ordem alfabética
    avi_files.sort()

    # Converte cada arquivo de vídeo AVI encontrado
    for filename in avi_files:
        file_path = os.path.join(output_path, filename)
        output_mp4 = os.path.join(output_dir_create('mp4'), filename + ".mp4")
        output_folder = os.path.dirname(output_mp4)

        try:
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
            print(f"\nVídeo convertido e salvo com sucesso.")
            print(f"Título do arquivo de vídeo AVI após a conversão para MP4: {filename}")
            print(f"Caminho onde está o arquivo de vídeo convertido para MP4: {output_folder}")
        except Exception as e:
            print(f"Erro ao executar o ffmpeg: {e}")

def convert_all_video():
    choice = input("\nVocê deseja converter os arquivos de vídeo AVI do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('avi') ########### Diretório onde os arquivos serão salvos e pesquisados
        converter_all_avi_mp4(output_path)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está os arquivos AVI (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print(f"\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input(f"Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print(f"\nO diretório informado ainda é inválido.")  
        converter_all_avi_mp4(output_path)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 11 do menu e tente novamente.")

if __name__ == "__main__":
    convert_all_video()