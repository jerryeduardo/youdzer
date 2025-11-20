import yt_dlp
from output_dir import output_dir_create

def download_youtube_clip_video(url, output_path, start_time, end_time):
    ydl_opts = {
        'format': 'bestvideo[height<=2160]+bestaudio/best',  # Baixa o melhor formato disponível
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Modelo de nome do arquivo
	    'merge_output_format': 'mp4',  # Mescla o vídeo e o áudio no formato mp4
        # Aqui definimos o corte usando regex de tempo
        'download_sections': {
            'sections': [f"*{start_time}-{end_time}"]        # Exemplo: "*00:01:00-00:02:30"
        }
    }

    try:
        print("Iniciando o download do corte de vídeo...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Obtemos o título da música do dicionário de informações
            title = info_dict.get('title', 'unknown')
            # Adiciona a extensão .mp4 ao final do título
            file_name = f"{title}.mp4"
            print(f"Corte baixado e salvo com sucesso. \nTítulo do arquivo MP4 baixado: \n{file_name}")
            return file_name
    except Exception as e:
            print("Ocorreu um erro ao baixar corte de vídeo do YouTube.")
            return None

def download_clip_video():
    output_path = output_dir_create('clips/mp4') # Diretório onde os arquivos serão salvos e pesquisados
    url = input("\nDigite a URL do vídeo do YouTube: ")
    start_time = input("Digite o tempo inicial (formato hh:mm:ss): ")
    end_time = input("Digite o tempo final (formato hh:mm:ss): ")
    download_youtube_clip_video(url, output_path, start_time, end_time)

if __name__ == "__main__":
    download_clip_video()