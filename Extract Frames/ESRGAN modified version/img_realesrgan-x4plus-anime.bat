@echo off
for %%a in (%*) do ("%~dp0"\realesrgan-ncnn-vulkan.exe   -i "%~1"   -o "%~dp1\%~n1"_x4plus-anime.jpg   -n realesrgan-x4plus-anime )
exit     