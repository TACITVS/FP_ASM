@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
set "BIN_DIR=bin"

if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo ========================================
echo Building Audio RMS Normalization Demo
echo ========================================
echo.
echo Compiling demo_audio_rms.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_audio_rms.c" "%OBJ_DIR%\fp_core_fused_folds.o" "%OBJ_DIR%\fp_core_fused_maps.o" -Iinclude -o "%BIN_DIR%\audio_rms.exe" -lm 2^>^&1
if exist "%BIN_DIR%\audio_rms.exe" (
    echo SUCCESS: audio_rms.exe created
    echo.
    echo ========================================
    echo Running Audio RMS Benchmark
    echo ========================================
    echo.
    echo Usage: audio_rms.exe [n_samples] [iterations]
    echo Example: audio_rms.exe 20000000 30
    echo.
    echo Running with defaults (10M samples, 50 iterations)...
    echo.
    "%BIN_DIR%\audio_rms.exe"
) else (
    echo FAILED: Could not create audio_rms.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
