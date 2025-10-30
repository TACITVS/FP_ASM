@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
set "BIN_DIR=bin"

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo Rebuilding bench_predicates.exe...
gcc "%DEMO_DIR%\demo_bench_predicates.c" "%OBJ_DIR%\fp_core_predicates.o" -Iinclude -o "%BIN_DIR%\bench_predicates.exe"
if exist "%BIN_DIR%\bench_predicates.exe" (
    echo SUCCESS: bench_predicates.exe created
    echo Running tests...
    "%BIN_DIR%\bench_predicates.exe" 100000 10
) else (
    echo FAILED: Could not create bench_predicates.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
