import ffmpeg
import os
from update_tags_artist_tracktitle import is_valid_directory
from output_dir import output_dir_create

def converter_avi_mp4(output_path, file_name_with_extension):
    # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
    # incluindo uma barra no meio das variáveis para acertar o caminho
    file_path = os.path.join(output_path, file_name_with_extension)
    output_mp4 = output_dir_create('mp4')
    
    try:
        ffmpeg.input(file_path).output(output_mp4, vcodec='libx264', acodec='aac').run()
        
        print(f"ok")
    except Exception as e:
        print(f"Erro ao executar o ffmpeg: {e}")

def convert_video():
    choice = input("\nVocê deseja converter um arquivo de vídeo AVI do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('avi') # Diretório onde os arquivos serão salvos e pesquisados
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .avi: ")
        converter_avi_mp4(output_path, file_name_with_extension)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está o arquivo de vídeo AVI (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print(f"\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input(f"Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print(f"\nO diretório informado ainda é inválido.")  
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .avi: ")
        converter_avi_mp4(output_path, file_name_with_extension)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 7 do menu e tente novamente.")

if __name__ == "__main__":
    convert_video()