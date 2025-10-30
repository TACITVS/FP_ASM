@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
set "BIN_DIR=bin"

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo ========================================
echo Building Moving Average Trading Demo
echo ========================================
echo.
echo Compiling demo_moving_avg.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_moving_avg.c" ^
    "%OBJ_DIR%\fp_core_reductions.o" ^
    "%OBJ_DIR%\fp_core_scans.o" ^
    -Iinclude -o "%BIN_DIR%\moving_avg.exe"
if exist "%BIN_DIR%\moving_avg.exe" (
    echo SUCCESS: moving_avg.exe created
    echo.
    echo ========================================
    echo Running Moving Average Benchmark
    echo ========================================
    echo.
    echo Usage: moving_avg.exe [n_prices] [iterations]
    echo Example: moving_avg.exe 5000000 50
    echo.
    echo Running with defaults (1M prices, 100 iterations)...
    echo.
    "%BIN_DIR%\moving_avg.exe"
) else (
    echo FAILED: Could not create moving_avg.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
