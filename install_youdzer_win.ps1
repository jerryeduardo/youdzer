Write-Output "Verificando instalação do Python e ffmpeg..."

# Verifica Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Output "Python não encontrado. Instalando via winget..."
    winget install -e --id Python.Python.3
} else {
    Write-Output "Python já está instalado."
}

# Verifica ffmpeg
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Output "ffmpeg não encontrado. Instalando via winget..."
    winget install -e --id Gyan.FFmpeg
} else {
    Write-Output "ffmpeg já está instalado."
}

$PYTHON_DESTINATION_DIR = "$env:USERPROFILE\youdzer"
$VENV_DIR = "$PYTHON_DESTINATION_DIR\yd-env"

Write-Output "Criando ambiente virtual em $VENV_DIR..."
python -m venv $VENV_DIR

Write-Output "Ativando ambiente virtual..."
& "$VENV_DIR\Scripts\Activate.ps1"

Write-Output "Instalando bibliotecas necessárias..."
pip install yt-dlp requests mutagen pillow ffmpeg-python

Write-Output "Copiando arquivos do projeto..."
New-Item -ItemType Directory -Force -Path $PYTHON_DESTINATION_DIR
Copy-Item *.py $PYTHON_DESTINATION_DIR

Write-Output "Criando pastas de saída..."
New-Item -ItemType Directory -Force -Path "$PYTHON_DESTINATION_DIR\mp3"
New-Item -ItemType Directory -Force -Path "$PYTHON_DESTINATION_DIR\mp4"
New-Item -ItemType Directory -Force -Path "$PYTHON_DESTINATION_DIR\avi"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Youdzer.lnk")
$Shortcut.TargetPath = "$PYTHON_DESTINATION_DIR\yd-env\Scripts\python.exe"
$Shortcut.Arguments = "$PYTHON_DESTINATION_DIR\index.py"
$Shortcut.IconLocation = "icons\512x512\youdzer.ico"
$Shortcut.Save()