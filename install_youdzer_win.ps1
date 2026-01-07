$pythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
$ffmpegExe = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
$ffmpegZip = "C:\ffmpeg.zip"
$pythonDestinationDir = "$env:USERPROFILE\Documents\YouDzer"
$venvDir = "$pythonDestinationDir\yd-env"
$startMenuDir = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
$startMenuShortcut = Join-Path $startMenuDir "YouDzer.lnk"
$desktopShortcut = "$env:USERPROFILE\Desktop\YouDzer.lnk"

function install_python_ffmpeg {
    Write-Output "Verificando se o Python, bem como o FFmpeg, estão instalados. Se não estiverem, a instalação será iniciada..."
    Start-Sleep -Seconds 1
    # Verifica Python
    try {
        if (Test-Path $pythonExe) {
            $pythonVersion = & $pythonExe --version
            Write-Output "Python já está instalado: ($pythonVersion)"
        } else {
            throw "Python não está instalado."
        }
    } catch {
        Write-Output "Python não está instalado. Instalando via winget..."
        winget install -e --id Python.Python.3.13
    }

    # Verifica FFmpeg
    try {
        if (Test-Path $ffmpegExe) {
            $ffmpegVersion = & $ffmpegExe -version | Out-String
            $versionInfo = (($ffmpegVersion -split "`n")[0] -replace "Copyright.*","").Trim()
            Write-Output "FFmpeg já está instalado: ($versionInfo)"
        } else {
            throw "FFmpeg não está instalado."
        }
    } catch {
        Write-Output "FFmpeg não está instalado. Instalando via github..."
        Write-Host "Encontrado " -NoNewline
        Write-Host "FFmpeg " -ForegroundColor Cyan -NoNewline
        Write-Host "[" -NoNewline
        Write-Host "Master.Latest.win64" -ForegroundColor Cyan -NoNewline
        Write-Output "]"
        install_ffmpeg
    }
}

function install_ffmpeg {
    Write-Output "Aguarde enquanto o FFmpeg está sendo baixado e instalado..."
    # URL da última release (sempre atualizada)
    $latestUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip"

    # Onde salvar o arquivo
    $outFile = "C:\ffmpeg.zip"

    # Baixa o zip
    Invoke-WebRequest -Uri $latestUrl -OutFile $outFile

    # Extrai para C:\ffmpeg
    Expand-Archive $outFile -DestinationPath "C:\ffmpeg" -Force

    # Exclui o zip após a extração
    if (Test-Path $ffmpegZip) {
        Remove-Item $ffmpegZip -Force 
    }

    # Adiciona ao PATH (para todos os usuários)
    $ffmpegPath = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$ffmpegPath", [System.EnvironmentVariableTarget]::Machine)

    # Testa a instalação
    $ffmpegVersion

    Write-Output "Instalado com êxito"
}

function install_venv_libs_files {
    Write-Output "Iniciando a criação do ambiente virtual do Python e a instalação das bibliotecas necessárias..."
    & $pythonExe -m venv $venvDir
    Write-Output "O ambiente virtual 'yd-env' foi criado no diretório $venvDir"

    & "$venvDir\Scripts\python.exe" -m pip install yt-dlp requests mutagen pillow ffmpeg-python
    Write-Output "As bibliotecas yt-dlp requests mutagen pillow ffmpeg-python foram instaladas."    

    Write-Output "Criação do ambiente virtual e a instalação das bibliotecas concluída com sucesso."

    Write-Output "Iniciando a instalação dos arquivos..."
    New-Item -ItemType Directory -Force -Path $pythonDestinationDir | Out-Null
    Copy-Item *.py $pythonDestinationDir
    Write-Output "Todos os arquivos .py foram copiados para $pythonDestinationDir"

    New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\mp3" | Out-Null
    New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\mp4" | Out-Null
    New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\avi" | Out-Null
    Write-Output "Os diretórios icons, mp3, mp4 e avi foram criados em $pythonDestinationDir"

    New-Item -ItemType Directory -Force -Path "$pythonDestinationDir\assets\icons\512x512" | Out-Null
    Copy-Item "assets\icons\512x512\youdzer.ico" "$pythonDestinationDir\assets\icons\512x512" -Force
    $WshShell = New-Object -ComObject WScript.Shell 
    $Shortcut = $WshShell.CreateShortcut($startMenuShortcut) 
    $Shortcut.TargetPath = "$pythonDestinationDir\yd-env\Scripts\python.exe"
    $Shortcut.Arguments = "$pythonDestinationDir\index.py"
    $Shortcut.IconLocation = "$pythonDestinationDir\assets\icons\512x512\youdzer.ico"
    $Shortcut.Save()
    Copy-Item $startMenuShortcut $desktopShortcut -Force
    Write-Output "O atalho do programa foi copiado para o Menu Iniciar e para a Área de Trabalho."

    Write-Output "Instalação dos arquivos concluída com sucesso."
    Write-Output "Instalação concluída com sucesso."
}

install_python_ffmpeg
install_venv_libs_files