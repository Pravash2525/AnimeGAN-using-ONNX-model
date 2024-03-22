@echo off
for %%a in (%*)  do  ("%~dp0"\realesrgan-ncnn-vulkan.exe   -i "%~1"    -o "%~dp1\%~n1"_x4plus.jpg     -n  realesrgan-x4plus )
exit