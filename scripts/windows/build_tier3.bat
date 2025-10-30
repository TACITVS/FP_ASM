@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
set "BIN_DIR=bin"

if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo ========================================
echo Building TIER 3 Test Suite
echo ========================================
echo.
echo [1/2] Compiling demo_tier3.c with fp_core_tier3.o...
gcc "%DEMO_DIR%\demo_tier3.c" "%OBJ_DIR%\fp_core_tier3.o" -Iinclude -o "%BIN_DIR%\tier3.exe" -v 2^>^&1

if errorlevel 1 (
    echo.
    echo ERROR: Compilation failed!
    popd >nul
    endlocal
    exit /b 1
)

echo.
echo [2/2] Build successful!
echo.
echo Executable: %BIN_DIR%\tier3.exe
echo.
echo Run with: %BIN_DIR%\tier3.exe
echo ========================================

popd >nul
endlocal
