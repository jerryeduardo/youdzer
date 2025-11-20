import os
import subprocess
import yt_dlp
from output_dir import output_dir_create

def cut_with_ffmpeg(full_path, output_path, title, start_time, duration):
    # Montando a sáida final do arquivo com a extensão .mp4 ao final do título
    cut_path = os.path.join(output_path, title + "_cut.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-ss", start_time,   # Seek rápido antes de -i
        "-i", full_path,
        "-t", duration,      # Duração do corte
        "-c:v", "libx264",
        "-c:a", "aac",
        cut_path
    ]
    print("\nIniciando corte do vídeo...")
    subprocess.run(cmd, check=True)
    return cut_path

def download_youtube_cut_video(url, output_path, start_time, duration):
    ydl_opts = {
        'format': 'bestvideo[height<=2160]+bestaudio/best',  # Baixa o melhor formato disponível
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Modelo de nome do arquivo
	    'merge_output_format': 'mp4',  # Mescla o vídeo e o áudio no formato mp4
    }

    try:
        print("\nIniciando o download do vídeo para posteriormente realizar o corte...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Obtemos o título da música do dicionário de informações
            title = info_dict.get('title', 'unknown')
            # Adiciona a extensão .mp4 ao final do título
            file_name = f"{title}.mp4"
            # Monta o caminho do arquivo .mp4
            full_path = os.path.join(output_path, file_name)
            # Realiza o corte e extrai o nome do arquivo com a extensão
            cut_file_name = os.path.basename(cut_with_ffmpeg(full_path, output_path, title, start_time, duration))
            print(f"\nVídeo cortado e salvo com sucesso. \nTítulo do arquivo MP4 após o corte: \n{cut_file_name}")
            return cut_file_name
    except Exception as e:
            print(f"Ocorreu um erro ao baixar o vídeo do YouTube. {e}")
            return None

def download_cut_video():
    output_path = output_dir_create('mp4/cuts') # Diretório onde os arquivos serão salvos e pesquisados
    url = input("\nDigite a URL do vídeo do YouTube: ")
    start_time = input("Digite o tempo de início do corte (formato hh:mm:ss): ")
    duration = input("Digite o tempo de duração do corte (formato hh:mm:ss): ")
    download_youtube_cut_video(url, output_path, start_time, duration)

if __name__ == "__main__":
    download_cut_video()