#!/bin/bash

uninstall_youdzer() {
    DESKTOP_FILE="youdzer.desktop"
    PYTHON_DESTINATION_DIR=""$HOME"/youdzer/"
    BASH_DESTINATION_DIR="/usr/local/bin/youdzer/"
    ICON_DESTINATION_DIR="/usr/share/icons/youdzer/"
    DESKTOP_DESTINATION_DIR=""$HOME"/.local/share/applications/"
    SOURCE_DIR="$(dirname "$0")"

    echo "Iniciando a desinstalação do ambiente virtual do Python 3, bem como das bibliotecas e arquivos (.py, .avi, .mp3, .mp4, ícone e executáveis)..."
    sleep 1  # Espera um segundo
    read -p "Você deseja desinstalar o Python? (Responda com 's' para sim ou 'n' para não): " respPython
    respPython=$(echo "$respPython" | tr '[:upper:]' '[:lower:]')
    if [[ "$respPython" == "s" ]] && command -v python3 &> /dev/null; then
        sudo apt remove -y python3
        echo "Desinstalado com êxito."
    else
        echo "Você optou por não desinstalar o Python."
    fi

    read -p "Você deseja desinstalar o FFmpeg? (Responda com 's' para sim ou 'n' para não): " respFFMpeg
    respFFMpeg=$(echo "$respFFMpeg" | tr '[:upper:]' '[:lower:]')
    if [[ "$respFFMpeg" == "s" ]] && command -v ffmpeg &> /dev/null; then
        ffmpegVersion=$($ffmpegExe -version | head -n 1)
        sudo apt remove -y ffmpeg
        echo "Desinstalado com êxito."
    else
        echo "Você optou por não desinstalar o FFmpeg."
    fi

    if [ -d "$PYTHON_DESTINATION_DIR" ]; then 
        sudo rm -rf "$PYTHON_DESTINATION_DIR"
        echo "Ambiente virtual do Python, bibliotecas e arquivos foram removidos."
    else 
        echo "Diretório $PYTHON_DESTINATION_DIR não foi encontrado." 
    fi

    if [ -d "$BASH_DESTINATION_DIR" ]; then 
        sudo rm -rf "$BASH_DESTINATION_DIR"
        echo "Arquivos extra de execução do programa foram removidos."
    else 
        echo "Diretório $BASH_DESTINATION_DIR não foi encontrado." 
    fi

    if [ -d "$ICON_DESTINATION_DIR" ]; then  
        sudo rm -rf "$ICON_DESTINATION_DIR" 
        echo "Ícone do programa foi removido."
    else 
        echo "Ícone do programa "$ICON_DESTINATION_DIR" não foi encontrado." 
    fi

    if [ -d "$DESKTOP_DESTINATION_DIR""$DESKTOP_FILE" ]; then 
        sudo rm -f "$DESKTOP_DESTINATION_DIR""$DESKTOP_FILE"
        echo "Arquivo executável do programa foi removido."
    else 
        echo "Arquivo executável "$DESKTOP_DESTINATION_DIR""$DESKTOP_FILE" não foi encontrado." 
    fi

    echo "Desinstalação concluída com sucesso."
}

uninstall_youdzer