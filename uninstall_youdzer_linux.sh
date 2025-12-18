#!/bin/bash

DESKTOP_FILE="youdzer.desktop"
PYTHON_DESTINATION_DIR=""$HOME"/youdzer/"
BASH_DESTINATION_DIR="/usr/local/bin/youdzer/"
ICON_DESTINATION_DIR="/usr/share/icons/youdzer/"
DESKTOP_DESTINATION_DIR=""$HOME"/.local/share/applications/"
SOURCE_DIR="$(dirname "$0")"

echo "Iniciando a desinstalação do ambiente virtual do Python 3, bem como das bibliotecas e arquivos (.py, mp3, mp4, ícone e executáveis)..."
sleep 1  # Espera meio segundo
sudo rm -rf "$PYTHON_DESTINATION_DIR"
sudo rm -rf "$BASH_DESTINATION_DIR"
sudo rm -rf "$ICON_DESTINATION_DIR"
sudo rm "$DESKTOP_DESTINATION_DIR""$DESKTOP_FILE"

echo "Desinstação concluída com sucesso."