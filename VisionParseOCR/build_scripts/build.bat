@echo off
echo ==========================
echo BUILD VISIONPARSEOCR
echo ==========================

REM limpar builds anteriores
rmdir /s /q build
rmdir /s /q dist

REM criar exe
python -m PyInstaller build_scripts/app.spec --clean

echo ==========================
echo BUILD FINALIZADO
echo ==========================
pause