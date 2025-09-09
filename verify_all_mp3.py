import os
import subprocess
from output_dir import output_dir_create
from update_tags_artist_tracktitle import is_valid_directory

def get_all_mp3_info(output_path):
    # Verifica se há arquivos MP3 no diretório
    mp3_files = [filename for filename in os.listdir(output_path) if filename.endswith('.mp3')]

    if not mp3_files:
        print("\nDiretório não possui arquivos MP3.")
        return
    
    # Ordenar os arquivos por ordem alfabética
    mp3_files.sort()

    # Verifica qualidade de cada arquivo MP3 encontrado
    for filename in mp3_files:
        file_path = os.path.join(output_path, filename)

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
                
                print(f"\n{filename}")
                print(f"Taxa de amostragem: {sample_rate / 1000} kHz")
                print(f"Taxa de bits: {bit_rate / 1000:.0f} kbps")
            else:
                print(f"\nArquivo MP3 encontrado: {(filename)}, mas a verificação da qualidade falhou.")
        except Exception as e:
            print(f"Erro ao executar o ffprobe: {e}")

def verify_all_audio():
    choice = input("\nVocê deseja verificar a qualidade dos arquivos MP3 do diretório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        get_all_mp3_info(output_path)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está os arquivos MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print("\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input("Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print("\nO diretório informado ainda é inválido.")
        get_all_mp3_info(output_path)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção 8 do menu e tente novamente.")

if __name__ == "__main__":
    verify_all_audio()