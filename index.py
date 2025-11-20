from download_youdzer_mp3 import download_youdzer_audio
from download_mp3 import download_audio
from download_mp4 import download_video
from download_playlist_mp3 import download_playlist_audio
from download_playlist_mp4 import download_playlist_video
from verify_mp3 import verify_audio
from verify_mp4 import verify_video
from verify_all_mp3 import verify_all_audio
from verify_all_mp4 import verify_all_video
from convert_avi_mp4 import convert_video
from convert_all_avi_mp4 import convert_all_video
from join_all_mp3 import join_all_audio
from update_tags_url import update_tags_url_audio
from update_tags_artist_tracktitle import update_tags_artist_tracktitle_audio
from update_tags_all_mp3 import update_tags_all_mp3_audio

def main_menu():
    while True:
        print("\n----------------------------------------------------------------------------v1.9")
        print("Menu:")
        print("1. Baixar música ou playlist do YouTube com atualização de metadados pelo Deezer")
        print("2. Baixar música do YouTube")
        print("3. Baixar vídeo do YouTube")
        print("4. Baixar corte de vídeo do YouTube")
        print("5. Baixar playlist de músicas do YouTube")
        print("6. Baixar playlist de vídeos do YouTube")
        print("7. Verificar a qualidade de um arquivo MP3")
        print("8. Verificar a qualidade de um arquivo MP4")
        print("9. Verificar a qualidade de todos os arquivos MP3 de um diretório")
        print("10. Verificar a qualidade de todos os arquivos MP4 de um diretório")
        print("11. Converter um arquivo AVI para MP4")
        print("12. Converter todos os arquivos AVI de um diretório para MP4")
        print("13. Juntar arquivos MP3 de um diretório para criar uma playlist e atualizar metadados pelo Deezer")
        print("14. Atualizar metadados pelo Deezer com base na URL da música")
        print("15. Atualizar metadados pelo Deezer com base no nome do artista e título da música")
        print("16. Atualizar metadados de todos os arquivos MP3 de um diretório pelo Deezer")
        print("17. Sair")
        
        choice = input("\nEscolha uma opção (1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16): ")
        
        if choice == '1':
            download_youdzer_audio()

        elif choice == '2':
            download_audio()

        elif choice == '3':
            download_video()

        elif choice == '4':
            download_clip_video()

        elif choice == '5':
            download_playlist_audio()

        elif choice == '6':
            download_playlist_video()

        elif choice == '7':
            verify_audio()

        elif choice == '8':
            verify_video()
        
        elif choice == '9':
            verify_all_audio()

        elif choice == '10':
            verify_all_video()

        elif choice == '11':
            convert_video()

        elif choice == '12':
            convert_all_video()

        elif choice == '13':
            join_all_audio()

        elif choice == '14':
            update_tags_url_audio()

        elif choice == '15':
            update_tags_artist_tracktitle_audio()

        elif choice == '16':
            update_tags_all_mp3_audio()

        elif choice == '17':
            print("Saindo...")
            break

if __name__ == "__main__":
    main_menu()