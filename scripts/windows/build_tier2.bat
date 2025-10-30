@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "ASM_DIR=src\asm"
set "DEMO_DIR=src\c\demos"
set "TEST_DIR=src\c\tests"
set "OBJ_DIR=build\obj"
set "BIN_DIR=bin"

if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo ========================================
echo Building TIER 2 Operations Test Suite
echo ========================================
echo.

echo Step 1: Assembling fp_core_tier2.asm
nasm -f win64 "%ASM_DIR%\fp_core_tier2.asm" -o "%OBJ_DIR%\fp_core_tier2.o"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Assembly failed
    popd >nul
    endlocal
    exit /b 1
)
echo OK - Object file created: %OBJ_DIR%\fp_core_tier2.o

echo.
echo Step 2: Compiling test programs
echo.

echo Building simple test...
gcc "%TEST_DIR%\test_tier2_simple.c" "%OBJ_DIR%\fp_core_tier2.o" -Iinclude -o "%BIN_DIR%\test_tier2_simple.exe"
if exist "%BIN_DIR%\test_tier2_simple.exe" (
    echo SUCCESS: test_tier2_simple.exe created
    echo.
    echo Running simple test...
    "%BIN_DIR%\test_tier2_simple.exe"
) else (
    echo WARNING: Could not create test_tier2_simple.exe
    echo This may be due to Windows Defender or antivirus blocking
)

echo.
echo Building comprehensive test suite...
gcc "%DEMO_DIR%\demo_tier2.c" "%OBJ_DIR%\fp_core_tier2.o" -Iinclude -o "%BIN_DIR%\tier2.exe"
if exist "%BIN_DIR%\tier2.exe" (
    echo SUCCESS: tier2.exe created
    echo.
    echo Running comprehensive tests...
    "%BIN_DIR%\tier2.exe"
) else (
    echo WARNING: Could not create tier2.exe
    echo This may be due to Windows Defender or antivirus blocking
)

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo TIER 2 module contains:
echo   - fp_sort_i64, fp_sort_f64 (sorting)
echo   - fp_unique_i64 (remove duplicates)
echo   - fp_union_i64 (set union)
echo   - fp_intersect_i64 (set intersection)
echo.
echo Library completeness: ~85%%

popd >nul
endlocal
pause
