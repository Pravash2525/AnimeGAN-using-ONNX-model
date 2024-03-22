@echo off
set "img_sequences=img_sequences"
set "scaled_images=scaled_images"

rem Create the mod_images directory if it doesn't exist
if not exist "%scaled_images%" mkdir "%scaled_images%"


for %%F in ("%img_sequences%\*.*") do (
    "%~dp0\realesrgan-ncnn-vulkan.exe"   -i "%%F"   -o "%scaled_images%\%%~nxF"_x4plus.png   -n realesrgan-x4plus 
)

exit













































