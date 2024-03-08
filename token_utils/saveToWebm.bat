@echo off
setlocal

:: Check for input parameter
if "%~1"=="" (
    echo Please provide the base file name as a parameter.
    echo Usage: %~nx0 [BaseFileName]
    goto :eof
)

:: Set the base file name
set "BASE_FILE_NAME=%~1"

:: Run FFmpeg command
ffmpeg -framerate 24 -i .\%BASE_FILE_NAME%_frames\%BASE_FILE_NAME%_%%d.png -c:v libvpx-vp9 -pix_fmt yuva420p %BASE_FILE_NAME%.webm

echo Conversion complete.
