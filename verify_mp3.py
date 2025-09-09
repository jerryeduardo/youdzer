import os
import subprocess
from output_dir import output_dir_create
from update_tags_artist_tracktitle import is_valid_directory

def get_mp3_info(output_path, file_name_with_extension):
    # Faz a junção do caminho do diretório com o nome do arquivo acrescido da extensão, 
    # incluindo uma barra no meio das variáveis para acertar o caminho
    file_path = os.path.join(output_path, file_name_with_extension)

    try:
        # Executa o comando ffprobe
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=sample_rate, bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Captura a saída do comando
        output = result.stdout.strip().split('\n')

        if len(output) >= 2:
            sample_rate = int(output[0])
            bit_rate = int(output[1])
            
            print(f"Taxa de amostragem: {sample_rate / 1000} kHz")
            print(f"Taxa de bits: {bit_rate / 1000:.0f} kbps")
        else:
            print(f"\nO arquivo {(file_name_with_extension)} não existe.")
    except Exception as e:
        print(f"Erro ao executar o ffprobe: {e}")

def verify_audio():
    choice = input("\nVocê deseja verificar a qualidade de um arquivo MP3 do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp3: ")
        get_mp3_info(output_path, file_name_with_extension)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está o arquivo MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")  
        file_name_with_extension = input("\nDigite o título do arquivo com a extensão .mp3: ")
        get_mp3_info(output_path, file_name_with_extension)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 6 do menu e tente novamente.")

if __name__ == "__main__":
    verify_audio()