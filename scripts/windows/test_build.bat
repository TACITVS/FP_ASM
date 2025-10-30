@echo off
setlocal
for %%I in ("%~dp0\..\..") do set "REPO_ROOT=%%~fI"
pushd "%REPO_ROOT%" >nul

set "DEMO_DIR=src\c\demos"
set "OBJ_DIR=build\obj"
if not exist "%OBJ_DIR%" mkdir "%OBJ_DIR%"
set "BIN_DIR=bin"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

gcc "%DEMO_DIR%\demo_audio_rms.c" "%OBJ_DIR%\fp_core_fused_folds.o" "%OBJ_DIR%\fp_core_fused_maps.o" -Iinclude -o "%BIN_DIR%\audio_rms.exe" -lm
if exist "%BIN_DIR%\audio_rms.exe" (
    echo SUCCESS: audio_rms.exe created
) else (
    echo FAILED: Could not create audio_rms.exe
)

popd >nul
endlocal
