import os
import subprocess
from output_dir import output_dir_create
from update_tags_artist_tracktitle import is_valid_directory

def get_mp4_info(output_path, file_name_with_extension):
    # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
    # incluindo uma barra no meio das variáveis para acertar o caminho
    file_path = os.path.join(output_path, file_name_with_extension)

    try:
        # Executa o comando ffprobe para obter largura, altura e bitrate do vídeo
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Captura a saída do comando
        output = result.stdout.strip().split('\n')

        if len(output) >= 3:
            width = int(output[0])
            height = int(output[1])
            bit_rate = int(output[2])	
            bit_rate_kbps = bit_rate / 1000
            
            # Classifica a resolução
            if width >= 3840 and height >= 2160:
                resolution = "4K (Ultra HD)"
            elif width >= 2560 and height >= 1440:
                resolution = "2K (QHD/WQHD)"
            elif width >= 1920 and height >= 1080:
                resolution = "1080p (Full HD)"
            elif width >= 1280 and height >= 720:
                resolution = "720p (HD)"
            elif width >= 854 and height >= 480:
                resolution = "480p (FWVGA)"
            elif width >= 640 and height >= 360:
                resolution = "360p (nHD)"
            elif width >= 426 and height >= 240:
                resolution = "240p (Low)"
            elif width >= 256 and height >= 144:
                resolution = "144p (Very Low)"
            else:
                resolution = "Resolução abaixo de 144p ou não catalogada no código"
            
            print(f"Resolução do vídeo: {width}x{height} ({resolution})")
            print(f"Taxa de bits: {bit_rate_kbps / 1000:.2f} Mbps")
        else:
            print(f"\nO arquivo {(file_name_with_extension)} não existe.")
    except Exception as e:
        print(f"Erro ao executar o ffprobe: {e}")

def verify_video():
    choice = input("\nVocê deseja verificar a qualidade de um arquivo MP4 do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp4') # Diretório onde os arquivos serão pesquisados
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp4: ")
        get_mp4_info(output_path, file_name_with_extension)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está o arquivo MP4 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")  
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp4: ")
        get_mp4_info(output_path, file_name_with_extension)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 7 do menu e tente novamente.")

if __name__ == "__main__":
    verify_video()