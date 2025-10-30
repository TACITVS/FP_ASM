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
echo Building K-Means Clustering Demo
echo ========================================
echo.
echo Compiling demo_kmeans.c with FP-ASM library...
gcc "%DEMO_DIR%\demo_kmeans.c" ^
    "%OBJ_DIR%\fp_core_reductions.o" ^
    "%OBJ_DIR%\fp_core_fused_folds.o" ^
    "%OBJ_DIR%\fp_core_fused_maps.o" ^
    -Iinclude -o "%BIN_DIR%\kmeans.exe" -lm
if exist "%BIN_DIR%\kmeans.exe" (
    echo SUCCESS: kmeans.exe created
    echo.
    echo ========================================
    echo Running K-Means Benchmark
    echo ========================================
    echo.
    echo Usage: kmeans.exe [n_points] [k_clusters] [dimensions] [iterations]
    echo Example: kmeans.exe 50000 5 16 20
    echo.
    echo Running with defaults (10000 points, 5 clusters, 16D, 50 iterations)...
    echo.
    "%BIN_DIR%\kmeans.exe"
) else (
    echo FAILED: Could not create kmeans.exe
    echo Please check if Windows Defender or antivirus is blocking gcc
)

popd >nul
endlocal
pause
