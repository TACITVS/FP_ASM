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
echo Building Partition Demo
echo ========================================
echo.
echo Assembling fp_core_compaction.asm...
nasm -f win64 "%ASM_DIR%\fp_core_compaction.asm" -o "%OBJ_DIR%\fp_core_compaction.o"

if exist "%OBJ_DIR%\fp_core_compaction.o" (
    echo SUCCESS: fp_core_compaction.o created
    echo.
    echo Building partition demo...
    gcc "%DEMO_DIR%\demo_partition.c" "%OBJ_DIR%\fp_core_compaction.o" -Iinclude -o "%BIN_DIR%\partition.exe"

    if exist "%BIN_DIR%\partition.exe" (
        echo SUCCESS: partition.exe created
        echo.
        echo ========================================
        echo Testing Partition - List FP Operation
        echo ========================================
        echo.
        "%BIN_DIR%\partition.exe"
    ) else (
        echo FAILED: Could not create partition.exe
    )
) else (
    echo FAILED: Could not assemble fp_core_compaction.o
)

popd >nul
endlocal
pause
