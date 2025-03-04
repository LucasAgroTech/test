@echo off
echo Iniciando o processo de empacotamento do Pipeline EMBRAPII SRInfo...
echo.

REM Verificar se o Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python nao encontrado. Por favor, instale o Python 3.x e tente novamente.
    pause
    exit /b 1
)

REM Executar o script de build
python build_app.py

REM Verificar se o processo foi concluído com sucesso
if %errorlevel% neq 0 (
    echo.
    echo Erro durante o processo de empacotamento. Verifique as mensagens acima.
    pause
    exit /b 1
)

echo.
echo Processo de empacotamento concluido com sucesso!
echo.
echo Para executar o aplicativo, navegue ate a pasta dist\pipeline_embrapii_srinfo e execute o arquivo "Pipeline EMBRAPII SRInfo.exe"
echo.
pause
