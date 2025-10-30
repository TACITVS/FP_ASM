@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "ASM_DIR=src\asm"
set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
set "BIN_DIR=bin"

if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo Building Algorithm #2: Percentile Calculations
echo.

echo Step 1: Assembling fp_core_percentiles.asm...
nasm -f win64 "%ASM_DIR%\fp_core_percentiles.asm" -o "%OBJ_DIR%\fp_core_percentiles.o"
if errorlevel 1 (
    echo ERROR: Assembly failed!
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Step 2: Compiling demo_percentiles.c...
echo (Linking with fp_core_percentiles.o and fp_core_tier2.o for sorting)
gcc "%DEMO_DIR%\demo_percentiles.c" "%OBJ_DIR%\fp_core_percentiles.o" "%OBJ_DIR%\fp_core_tier2.o" -Iinclude -o "%BIN_DIR%\percentiles.exe"
if errorlevel 1 (
    echo ERROR: Compilation failed!
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Build successful! Run with: %BIN_DIR%\percentiles.exe

popd >nul
endlocal
