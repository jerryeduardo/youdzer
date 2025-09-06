from pydub import AudioSegment
import os
from update_tags_artist_tracktitle import is_valid_directory
from output_dir import output_dir_create

def joinup_all_mp3(output_path):
    # Verifica se há arquivos MP3 no diretório
    mp3_files = [filename for filename in os.listdir(output_path) if filename.endswith('.mp3')]

    if not mp3_files:
        print("\nDiretório não possui arquivos MP3.")
        return
    
    # Ordenar os arquivos por ordem alfabética
    mp3_files.sort()

    # Inicializa o áudio final como vazio
    audio_final = AudioSegment.empty()

    # Junta cada arquivo de música MP3 encontrado
    for filename in mp3_files:
        file_path = os.path.join(output_path, filename)
        try:
            print(f"Adicionando: {filename}")
            audio = AudioSegment.from_mp3(file_path)
            audio_final += audio
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")

    # Exporta o áudio final unido
    output_file = os.path.join(output_path, "audio_unido.mp3")
    try:
        audio_final.export(output_file, format="mp3")
        print(f"\nArquivo final criado com sucesso: {output_file}")
    except Exception as e:
        print(f"Erro ao exportar o arquivo final: {e}")

def join_all_audio():
    choice = input("\nVocê deseja juntar os arquivos de música MP3 do direetório padrão? (Responda com 's' para sim ou 'n' para não): ").lower()
    if choice == 's':
        output_path = output_dir_create('mp3') # Diretório onde os arquivos serão pesquisados
        joinup_all_mp3(output_path)
    elif choice == 'n':
        output_path = input("\nInforme o caminho do diretório onde está os arquivos MP3 (Exemplo: /home/seuusuario/Downloads/): ")
        if not is_valid_directory(output_path):
            print(f"\nO caminho informado para o diretório é inválido.")
            while not is_valid_directory(output_path):
                output_path = input(f"Por favor, informe o caminho válido para o diretório: ")
                if not is_valid_directory(output_path):
                    print(f"\nO diretório informado ainda é inválido.")  
        joinup_all_mp3(output_path)
    else: 
        print("\nVocê inseriu uma informação incorreta. Por favor, acesse a opção ? do menu e tente novamente.")

if __name__ == "__main__":
    join_all_audio()