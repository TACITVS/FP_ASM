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

echo Building Algorithm #5: Outlier Detection
echo.

echo Step 1: Assembling fp_core_outliers.asm...
nasm -f win64 "%ASM_DIR%\fp_core_outliers.asm" -o "%OBJ_DIR%\fp_core_outliers.o"
if errorlevel 1 (
    echo ERROR: Assembly failed!
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Step 2: Compiling demo_outliers.c...
echo (Linking with fp_core_outliers.o and fp_core_percentiles.o for IQR method)
gcc "%DEMO_DIR%\demo_outliers.c" "%OBJ_DIR%\fp_core_outliers.o" "%OBJ_DIR%\fp_core_percentiles.o" -Iinclude -o "%BIN_DIR%\outliers.exe"
if errorlevel 1 (
    echo ERROR: Compilation failed!
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Build successful! Run with: %BIN_DIR%\outliers.exe

popd >nul
endlocal
