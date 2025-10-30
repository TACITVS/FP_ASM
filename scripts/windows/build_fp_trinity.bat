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
echo Building FP Trinity Test
echo ========================================
echo.
echo Compiling demo_fp_trinity.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_fp_trinity.c" ^
    "%OBJ_DIR%\fp_core_fused_maps.o" ^
    "%OBJ_DIR%\fp_core_reductions.o" ^
    "%OBJ_DIR%\fp_core_fused_folds.o" ^
    "%OBJ_DIR%\fp_core_scans.o" ^
    -Iinclude -o "%BIN_DIR%\fp_trinity.exe"
if exist "%BIN_DIR%\fp_trinity.exe" (
    echo SUCCESS: fp_trinity.exe created
    echo.
    echo ========================================
    echo Running FP Trinity Test
    echo ========================================
    echo.
    echo This tests Map, ZipWith, Fold, Scan
    echo.
    "%BIN_DIR%\fp_trinity.exe"
) else (
    echo FAILED: Could not create fp_trinity.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
