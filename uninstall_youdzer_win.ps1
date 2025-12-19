$pythonDestinationDir = "$env:USERPROFILE\Documents\YouDzer"
$startMenuShortcut = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\YouDzer.lnk" 
$desktopShortcut = "$env:USERPROFILE\Desktop\YouDzer.lnk"

Write-Output "Iniciando a desinstalação do ambiente virtual do Python, bem como das bibliotecas e arquivos (.py, .avi, .mp3, .mp4 e atalhos)..." 
Start-Sleep -Seconds 1 # Espera um segundo
if (Test-Path $pythonDestinationDir) {
    Remove-Item $pythonDestinationDir -Recurse -Force 
}
if (Test-Path $startMenuShortcut) {
    Remove-Item $startMenuShortcut -Force 
}
if (Test-Path $desktopShortcut) {
    Remove-Item $desktopShortcut -Force 
}

Write-Output "Desinstalação concluída com sucesso."