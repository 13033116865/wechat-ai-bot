@echo off
setlocal enabledelayedexpansion

REM Copy project to Desktop\WeChatAssistant (excluding .git and venv folders)

set "SRC=%~dp0.."
for %%I in ("%SRC%") do set "SRC=%%~fI"

set "DEST=%USERPROFILE%\Desktop\WeChatAssistant"

echo Source: %SRC%
echo Dest:   %DEST%

if exist "%DEST%" rmdir /S /Q "%DEST%"
mkdir "%DEST%"

REM Use robocopy when available
where robocopy >nul 2>nul
if %errorlevel%==0 (
  robocopy "%SRC%" "%DEST%" /E /XD ".git" "venv" ".venv" "__pycache__" ".pytest_cache" ".mypy_cache" ".ruff_cache" >nul
) else (
  xcopy "%SRC%\*" "%DEST%\" /E /I /Y >nul
)

echo.
echo Copied to: %DEST%
echo Next:
echo   cd /d "%DEST%"
echo   copy .env.example .env
echo   python -m venv .venv
echo   .venv\Scripts\activate
echo   pip install -r requirements.txt
echo   python app.py

endlocal

