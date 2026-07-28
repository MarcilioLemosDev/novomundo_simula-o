@echo off
chcp 65001 >nul
title Novo Mundo
cls

REM Entra na pasta onde ESTE arquivo esta, seja ela qual for.
REM E o que resolve o erro mais comum de todos: rodar o comando do lugar errado.
cd /d "%~dp0"

REM Descobre como o Python se chama nesta maquina.
set PY=py
%PY% --version >nul 2>&1
if errorlevel 1 set PY=python
%PY% --version >nul 2>&1
if errorlevel 1 goto sempython

echo.
echo   Novo Mundo - preparando...
echo.

REM Garante o branch certo e o codigo mais novo. Sem git, segue assim mesmo.
git checkout claude/neural-model-design-qxqxsn >nul 2>&1
git pull >nul 2>&1

REM Instala as duas dependencias. Se ja estiverem, nao custa nada.
%PY% -m pip install -q -r requirements.txt

echo   Abrindo no navegador.
echo   Para encerrar, feche esta janela.
echo.

%PY% -m streamlit run app.py
goto fim

:sempython
echo.
echo   Python nao encontrado nesta maquina.
echo.
echo   Baixe em  python.org/downloads
echo   e na PRIMEIRA tela do instalador marque a caixa
echo   "Add python.exe to PATH", embaixo.
echo.
echo   Depois feche esta janela e clique aqui de novo.
echo.

:fim
pause
