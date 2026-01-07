function uninstall_youdzer{
    $pythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
    $ffmpegExe = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
    $ffmpegDestinationDir = "C:\ffmpeg"
    $pythonDestinationDir = "$env:USERPROFILE\Documents\YouDzer"
    $startMenuShortcut = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\YouDzer.lnk" 
    $desktopShortcut = "$env:USERPROFILE\Desktop\YouDzer.lnk"

    Write-Output "Iniciando a desinstalação do Python, FFmpeg, ambiente virtual do Python, bem como das bibliotecas e arquivos (.py, .avi, .mp3, .mp4 e atalhos)..." 
    Start-Sleep -Seconds 1 # Espera um segundo

    $respPython = Read-Host "Você deseja desinstalar o Python? (Responda com 's' para sim ou 'n' para não)"
    $respPython = $respPython.ToLower()
    if (($respPython -eq "s") -and (Test-Path $pythonExe)) {
        winget uninstall -e --id Python.Python.3.13
    } else {
        Write-Output "Você optou por não desinstalar o Python."
    }

    $respFFMpeg = Read-Host "Você deseja desinstalar o FFmpeg? (Responda com 's' para sim ou 'n' para não)"
    $respPython = $respPython.ToLower()
    if (($respFFMpeg -eq "s") -and (Test-Path $ffmpegExe)) {
        $ffmpegVersion = & $ffmpegExe -version | Out-String
        $versionInfo = (($ffmpegVersion -split "`n")[0] -replace "Copyright.*","").Trim()
        Write-Host "Encontrado " -NoNewline 
        Write-Host "[" -NoNewline 
        Write-Host "$versionInfo" -ForegroundColor Cyan -NoNewline
        Write-Output "]"
        Write-Output "Iniciando a desinstalação do pacote..."
        Remove-Item $ffmpegDestinationDir -Recurse -Force
        uninstall_ffmpegPATH
    } else {
        Write-Output "Você optou por não desinstalar o FFmpeg."
    }

    if (Test-Path $pythonDestinationDir) {
        Remove-Item $pythonDestinationDir -Recurse -Force
        Write-Output "Ambiente virtual do Python, bibliotecas e arquivos foram removidos."
    } else {
        Write-Output "Diretório $pythonDestinationDir não foi encontrado." 
    }

    if (Test-Path $startMenuShortcut) {
        Remove-Item $startMenuShortcut -Force 
        Write-Output "Atalho do Menu Iniciar foi removido."
    } else {
        Write-Output "Atalho do Menu Iniciar $startMenuShortcut não foi encontrado."
    }
    
    if (Test-Path $desktopShortcut) {
        Remove-Item $desktopShortcut -Force 
        Write-Output "Atalho da Área de Trabalho foi removido."
    } else {
        Write-Output "Atalho da Área de Trabalho $desktopShortcut não foi encontrado."
    }

    Write-Output "Desinstalação concluída com sucesso."
}

function uninstall_ffmpegPATH {
    # Caminho que você quer remover
    $ffmpegPath = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"

    # Pega o PATH atual do sistema
    $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)

    # Divide em entradas, remove o caminho do FFmpeg e junta de novo
    $newPath = ($currentPath -split ";" | Where-Object { $_ -ne $ffmpegPath }) -join ";"

    # Atualiza a variável PATH
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)

    # Write-Output "Entrada removida do PATH: $ffmpegPath"
    Write-Output "Desinstalado com êxito"
}

uninstall_youdzer