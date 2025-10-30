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

echo Building FP-ASM List FP Early-Exit Operations Test Suite...
echo.

echo Step 1: Assembling fp_core_compaction.asm
nasm -f win64 "%ASM_DIR%\fp_core_compaction.asm" -o "%OBJ_DIR%\fp_core_compaction.o"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Assembly failed
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Step 2: Compiling and linking demo_take_drop.c
gcc "%DEMO_DIR%\demo_take_drop.c" "%OBJ_DIR%\fp_core_compaction.o" -Iinclude -o "%BIN_DIR%\demo_take_drop.exe"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Compilation failed
    popd >nul
    endlocal
    exit /b 1
)
echo OK

echo.
echo Step 3: Running tests and benchmarks
"%BIN_DIR%\demo_take_drop.exe" 10000000 10

echo.
echo Build complete!

popd >nul
endlocal
