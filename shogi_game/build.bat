@echo off
REM Shogi Game Build Script (Windows)
REM This script creates an EXE file using PyInstaller
setlocal EnableExtensions EnableDelayedExpansion

REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo Shogi Game Build Script
echo ========================================
echo.
echo Working Directory: %CD%
echo.

REM Check required packages
echo [1/6] Checking required packages...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed.
    echo Install now? [Y/n]
    set /p install_pyinstaller=
    if /i "%install_pyinstaller%"=="Y" (
        pip install pyinstaller
    ) else (
        echo Build cancelled.
        pause
        exit /b 1
    )
)

python -c "import PySide6" 2>nul
if errorlevel 1 (
    echo PySide6 is not installed.
    echo Install now? [Y/n]
    set /p install_pyside=
    if /i "%install_pyside%"=="Y" (
        pip install PySide6
    ) else (
        echo Build cancelled.
        pause
        exit /b 1
    )
)

python -c "import PIL" 2>nul
if errorlevel 1 (
    echo Pillow is not installed.
    echo Install now? [Y/n]
    set /p install_pillow=
    if /i "%install_pillow%"=="Y" (
        pip install Pillow
    ) else (
        echo Build cancelled.
        pause
        exit /b 1
    )
)

echo All required packages are installed.
echo.

REM Check and generate icon file
echo [2/6] Checking icon file...
if not exist "assets\icons\shogi_icon.ico" (
    echo Icon file not found.
    echo Generating from PNG...
    if exist "assets\icons\将棋ゲームアイコン.png" (
        python convert_icon.py
        if errorlevel 1 (
            echo Warning: Icon generation failed.
            echo Build will continue with default icon.
        ) else (
            echo Icon generated successfully.
        )
    ) else (
        echo Warning: PNG image not found.
        echo Build will continue with default icon.
    )
) else (
    echo Icon file found: assets\icons\shogi_icon.ico
)
echo.

REM Remove old build files
echo [3/6] Removing old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Cleanup complete.
echo.

REM Run PyInstaller
echo [4/6] Building with PyInstaller...
echo This may take several minutes.
echo.
pyinstaller shogi_game.spec

if errorlevel 1 (
    echo.
    echo Error: Build failed.
    echo Please check error messages above.
    pause
    exit /b 1
)

echo.
echo Build complete!
echo.

REM Check generated files
echo [5/6] Checking generated files...
set OUTPUT_EXE=
if exist "dist\将棋ゲーム.exe" set OUTPUT_EXE=dist\将棋ゲーム.exe
if not defined OUTPUT_EXE if exist "dist\ShogiGame.exe" set OUTPUT_EXE=dist\ShogiGame.exe

REM Fallback: dist 配下の exe を自動検出（onedir 構成にも対応）
if not defined OUTPUT_EXE (
    for /r dist %%F in (*.exe) do (
        set OUTPUT_EXE=%%F
        goto :found_exe
    )
)

:found_exe

if defined OUTPUT_EXE (
    echo Generated file found: !OUTPUT_EXE!
    for %%I in ("!OUTPUT_EXE!") do echo File size: %%~zI bytes
) else (
    echo Error: Generated executable not found in dist\
    if exist dist (
        echo Dist directory contents:
        dir /b dist
    ) else (
        echo Dist directory does not exist.
    )
    pause
    exit /b 1
)
echo.

REM Create distribution package
echo [6/6] Creating distribution package...
set VERSION=1.0.0
set PACKAGE_NAME=ShogiGame_v%VERSION%_Windows

if exist "%PACKAGE_NAME%" rmdir /s /q "%PACKAGE_NAME%"
mkdir "%PACKAGE_NAME%"

copy "!OUTPUT_EXE!" "%PACKAGE_NAME%\ShogiGame.exe"
copy "README.md" "%PACKAGE_NAME%\"
copy "Docs\USER_GUIDE.md" "%PACKAGE_NAME%\UserGuide.md"

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Working Directory: %CD%
echo.
echo Generated files:
echo   - %CD%\!OUTPUT_EXE!
echo   - %CD%\%PACKAGE_NAME%\
echo.
echo Next steps:
echo   1. Test: !OUTPUT_EXE!
echo   2. Distribute: ZIP the %PACKAGE_NAME% folder
echo   OR
echo   3. Create installer with Inno Setup
echo      (See Docs\BUILD_DISTRIBUTION.md for details)
echo.
pause
endlocal
