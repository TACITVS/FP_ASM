@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "TEST_DIR=src\c\tests"
set "OBJ_DIR=build\obj"
if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
set "BIN_DIR=bin"

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo ========================================
echo Building Comprehensive Test Suite
echo ========================================
echo.
echo Compiling test_comprehensive.c with all modules...
gcc "%TEST_DIR%\test_comprehensive.c" ^
    "%OBJ_DIR%\fp_core_reductions.o" ^
    "%OBJ_DIR%\fp_core_fused_folds.o" ^
    "%OBJ_DIR%\fp_core_fused_maps.o" ^
    "%OBJ_DIR%\fp_core_simple_maps.o" ^
    "%OBJ_DIR%\fp_core_scans.o" ^
    "%OBJ_DIR%\fp_core_predicates.o" ^
    -Iinclude -o "%BIN_DIR%\test_comprehensive.exe"
if exist "%BIN_DIR%\test_comprehensive.exe" (
    echo SUCCESS: test_comprehensive.exe created
    echo.
    echo ========================================
    echo Running Comprehensive Tests
    echo ========================================
    echo.
    "%BIN_DIR%\test_comprehensive.exe"
    echo.
    echo ========================================
    echo Test run completed
    echo ========================================
) else (
    echo FAILED: Could not create test_comprehensive.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
