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
echo Building Monte Carlo Options Pricing Demo
echo ========================================
echo.
echo Compiling demo_monte_carlo.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_monte_carlo.c" ^
    "%OBJ_DIR%\fp_core_reductions.o" ^
    "%OBJ_DIR%\fp_core_fused_maps.o" ^
    -Iinclude -o "%BIN_DIR%\monte_carlo.exe" -lm
if exist "%BIN_DIR%\monte_carlo.exe" (
    echo SUCCESS: monte_carlo.exe created
    echo.
    echo ========================================
    echo Running Monte Carlo Benchmark
    echo ========================================
    echo.
    echo Usage: monte_carlo.exe [n_paths] [n_steps] [iterations]
    echo Example: monte_carlo.exe 5000000 252 5
    echo.
    echo Running with defaults (1M paths, 252 steps, 10 iterations)...
    echo.
    "%BIN_DIR%\monte_carlo.exe"
) else (
    echo FAILED: Could not create monte_carlo.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
