FROM mcr.microsoft.com/windows/servercore:ltsc2019

RUN [ "powershell.exe",  "-Command", "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex" ]
RUN choco feature enable --name allowGlobalConfirmation
RUN choco feature disable --name showDownloadProgress

RUN choco install python --version=3.8.6

ENTRYPOINT [ "powershell" ]