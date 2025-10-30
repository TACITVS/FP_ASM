@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
set "BIN_DIR=bin"

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo Rebuilding bench_fused_folds.exe...
gcc "%DEMO_DIR%\demo_bench_fused_folds.c" "%OBJ_DIR%\fp_core_fused_folds.o" -Iinclude -o "%BIN_DIR%\bench_fused_folds.exe"
if exist "%BIN_DIR%\bench_fused_folds.exe" (
    echo SUCCESS: bench_fused_folds.exe created
    echo Running tests...
    "%BIN_DIR%\bench_fused_folds.exe" 100000 5
) else (
    echo FAILED: Could not create bench_fused_folds.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
