# YouDzer
<p align="center">
    <img src="https://github.com/jerryeduardo/youdzer/blob/main/preview.png" width="50%" height="50%" alt="image" />
</p>
<p>
    O <b>YouDzer</b> é uma ferramenta que simplifica o download de músicas e vídeos do YouTube. Além disso, oferece verificação da qualidade dos arquivos baixados e permite a atualização dos metadados das músicas utilizando informações do Deezer.
</p>

## Instalação no sistema operacional Debian e derivados
Primeiramente, execute o Terminal<br>
Se o pacote Git não estiver instalado, inicie o processo de instalação com:
```
sudo apt install -y git
```
Agora, clone este repositório:
```
cd ~/Downloads/
git clone https://github.com/jerryeduardo/youdzer
```
Vá para o diretório youdzer:
```
cd ~/Downloads/youdzer/
```
Por fim, rode o comando de instalação:
```
./install_youdzer_linux.sh
```
Agora você pode usar o YouDzer em seu sistema acessando o menu de aplicativos e clicando no ícone do YouDzer.

## Desinstalação
Se desejar desinstalar o YouDzer, você pode fazê-lo executando o arquivo uninstall_youdzer_linux.sh, com:
```
./uninstall_youdzer_linux.sh
```

## Instalação no sistema operacional Windows 10 e 11
Primeiramente, execute o PowerShell como administrador<br>
Se o pacote Git não estiver instalado, inicie o processo de instalação com:
```
winget install -e --id Git.Git
```
Agora, clone este repositório:
```
cd $env:USERPROFILE\Downloads 
git clone https://github.com/jerryeduardo/youdzer
```
Se for a primeira vez rodando scripts, habilite a execução com:
```
Set-ExecutionPolicy RemoteSigned
```
Vá para o diretório youdzer:
```
cd $env:USERPROFILE\Downloads\youdzer
```
Por fim, rode o comando de instalação:
```
.\install_youdzer_win.ps1
```

## Desinstalação
Se desejar desinstalar o YouDzer, você pode fazê-lo executando o arquivo uninstall_youdzer_win.ps1, com:
```
.\uninstall_youdzer_win.ps1
```