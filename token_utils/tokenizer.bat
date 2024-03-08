@echo off
setlocal

:: Check for input GIF file
if "%~1"=="" (
    echo Please provide the GIF file name as a parameter.
    echo Usage: %~nx0 filename.gif
    goto :eof
)

:: Set the input GIF file name
set "GIF_FILE=%~1"

:: Extract the base name from the GIF file for the output sequence
set "BASE_NAME=%~n1"

:: Create a directory for the PNG sequence
if not exist "%BASE_NAME%_frames" mkdir "%BASE_NAME%_frames"

:: Run FFmpeg command to convert the GIF to a PNG sequence
ffmpeg -i "%GIF_FILE%" "%BASE_NAME%_frames\%BASE_NAME%_%%d.png"

echo Conversion to PNG sequence complete.

:: Run FFmpeg command
ffmpeg -framerate 6 -i .\%BASE_NAME%_frames\%BASE_NAME%_%%d.png -c:v libvpx-vp9 -pix_fmt yuva420p %BASE_NAME%.webm

echo Conversion complete.