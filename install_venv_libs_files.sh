#!/bin/bash

BASH_FILE="youdzer.sh"
ICON_FILE="icons/512x512/youdzer.svg"
DESKTOP_FILE="youdzer.desktop"
PYTHON_DESTINATION_DIR=""$HOME"/youdzer/"
BASH_DESTINATION_DIR="/usr/local/bin/youdzer/"
ICON_DESTINATION_DIR="/usr/share/icons/youdzer/icons/512x512/"
DESKTOP_DESTINATION_DIR=""$HOME"/.local/share/applications/"
VIRTUAL_ENV="yd-env/bin/activate"
SOURCE_DIR="$(dirname "$0")"

echo "Iniciando a criação do ambiente virtual do Python 3 e a instalação das bibliotecas necessárias..."
sleep 1  # Espera meio segundo
mkdir -p "$PYTHON_DESTINATION_DIR"
python3 -m venv "$PYTHON_DESTINATION_DIR"yd-env
echo "O ambiente virtual 'yd-env' criado no diretório $PYTHON_DESTINATION_DIR"

sleep 0.5  # Espera meio segundo
source "$PYTHON_DESTINATION_DIR""$VIRTUAL_ENV"
pip install yt-dlp requests mutagen pillow ffmpeg-python
echo "As bibliotecas yt-dlp requests mutagen pillow ffmpeg-python foram instaladas."

echo "Criação do ambiente virtual e a instalação das bibliotecas concluída com sucesso."

echo "Iniciando a instalação dos arquivos..."
sleep 1  # Espera 1 segundo
cp *.py "$PYTHON_DESTINATION_DIR"
echo "Todos os arquivos .py foram copiados para $PYTHON_DESTINATION_DIR"

sleep 0.5  # Espera meio segundo
sudo mkdir -p "$BASH_DESTINATION_DIR"
sudo cp "$BASH_FILE" "$BASH_DESTINATION_DIR"
echo "O arquivo bash do programa foi copiado para $BASH_DESTINATION_DIR"

sleep 0.5  # Espera meio segundo
mkdir -p "$PYTHON_DESTINATION_DIR/mp3"
mkdir -p "$PYTHON_DESTINATION_DIR/mp4"
mkdir -p "$PYTHON_DESTINATION_DIR/avi"
echo "Os diretórios mp3, mp4 e avi foram criados em $PYTHON_DESTINATION_DIR"

sleep 0.5  # Espera meio segundo
sudo mkdir -p "$ICON_DESTINATION_DIR"
sudo cp "$ICON_FILE" "$ICON_DESTINATION_DIR"
echo "O ícone do programa foi copiado para $ICON_DESTINATION_DIR"

sleep 0.5  # Espera meio segundo
cp "$DESKTOP_FILE" "$DESKTOP_DESTINATION_DIR"
echo "O arquivo executável do programa e foi copiado para $DESKTOP_DESTINATION_DIR"

echo "Instalação dos arquivos concluída com sucesso."