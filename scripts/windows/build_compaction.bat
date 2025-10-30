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

echo ========================================
echo Building Stream Compaction Module
echo ========================================
echo.
echo Assembling fp_core_compaction.asm...
nasm -f win64 "%ASM_DIR%\fp_core_compaction.asm" -o "%OBJ_DIR%\fp_core_compaction.o"

if exist "%OBJ_DIR%\fp_core_compaction.o" (
    echo SUCCESS: fp_core_compaction.o created
    echo.
    echo ========================================
    echo Building Filter Demo with REAL SIMD
    echo ========================================
    echo.
    gcc "%DEMO_DIR%\demo_filter.c" "%OBJ_DIR%\fp_core_reductions.o" "%OBJ_DIR%\fp_core_compaction.o" -Iinclude -o "%BIN_DIR%\filter_simd.exe"

    if exist "%BIN_DIR%\filter_simd.exe" (
        echo SUCCESS: filter_simd.exe created
        echo.
        echo ========================================
        echo Testing "List FP" Fitness
        echo ========================================
        echo.
        echo This will determine if the library can achieve
        echo "List FP" status with real SIMD compaction!
        echo.
        "%BIN_DIR%\filter_simd.exe"
    ) else (
        echo FAILED: Could not create filter_simd.exe
    )
) else (
    echo FAILED: Could not assemble fp_core_compaction.o
    echo Check NASM installation
)

popd >nul
endlocal
pause
