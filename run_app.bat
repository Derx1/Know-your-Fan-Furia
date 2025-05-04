@echo off
:: Mudar para o diretório do script
cd /d "%~dp0"

:: Configurar variáveis de ambiente
set FLASK_APP=app.py
set FLASK_ENV=production
set FLASK_DEBUG=0

:: Registrar início em arquivo de log
echo [%date% %time%] Iniciando aplicativo Flask >> app_log.txt

:: Tentar iniciar o servidor
echo Iniciando servidor Flask...
python app.py >> app_log.txt 2>&1

:: Se o servidor falhar, registrar o erro
if %errorlevel% neq 0 (
    echo [%date% %time%] ERRO: Servidor encerrou com código %errorlevel% >> app_log.txt
    exit /b %errorlevel%
)