$pythonDestinationDir = "$env:USERPROFILE\Documents\YouDzer"
$venvDir = "$pythonDestinationDir\yd-env"
$startMenuDir = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
$startMenuShortcut = Join-Path $startMenuDir "YouDzer.lnk"
$desktopShortcut = "$env:USERPROFILE\Desktop\YouDzer.lnk"

Write-Output "Verificando instalação do Python e ffmpeg..."
Start-Sleep -Seconds 1
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

Write-Output "Criando ambiente virtual em $venvDir..."
python -m venv $venvDir

Write-Output "Ativando ambiente virtual..."
. "$venvDir\Scripts\Activate.ps1"

Write-Output "Instalando bibliotecas necessárias..."
# $venvDir\Scripts\python.exe -m pip install yt-dlp requests mutagen pillow ffmpeg-python
pip install yt-dlp requests mutagen pillow ffmpeg-python

Write-Output "Copiando arquivos do programa..."
New-Item -ItemType Directory -Force -Path $pythonDestinationDir
Copy-Item *.py $pythonDestinationDir

Write-Output "Criando pastas de saída..."
New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\mp3"
New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\mp4"
New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\avi"

Write-Output "Criando atalho no Menu Iniciar e copiando para a Área de Trabalho..."
$WshShell = New-Object -ComObject WScript.Shell 
$Shortcut = $WshShell.CreateShortcut($startMenuShortcut) 
$Shortcut.TargetPath = "$pythonDestinationDir\yd-env\Scripts\python.exe"
$Shortcut.Arguments = "$pythonDestinationDir\index.py"
$Shortcut.IconLocation = "icons\512x512\youdzer.ico"
$Shortcut.Save()
Copy-Item $startMenuShortcut $desktopShortcut -Force