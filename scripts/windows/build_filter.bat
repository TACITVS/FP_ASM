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
echo Building Filter FP Fitness Demo
echo ========================================
echo.
echo Compiling demo_filter.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_filter.c" "%OBJ_DIR%\fp_core_reductions.o" -Iinclude -o "%BIN_DIR%\filter.exe" 2^>^&1
if exist "%BIN_DIR%\filter.exe" (
    echo SUCCESS: filter.exe created
    echo.
    echo ========================================
    echo Running Filter FP Benchmark
    echo ========================================
    echo.
    echo Usage: filter.exe [n_elements] [iterations]
    echo Example: filter.exe 20000000 30
    echo.
    echo Running with defaults (10M elements, 50 iterations)...
    echo.
    "%BIN_DIR%\filter.exe"
) else (
    echo FAILED: Could not create filter.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
