@echo off
echo Initializing project environment...
call uv sync

echo .
call migrate.bat

echo .
call frontend-initialize.bat

echo Project Setup Complete!

pause