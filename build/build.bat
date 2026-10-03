@echo off
REM Build EduPaie.exe et, si Inno Setup est installe, son installateur Windows.

echo ========================================
echo Build EduPaie avec PyInstaller
echo ========================================
echo.

pushd "%~dp0.."

REM Vérifier si PyInstaller est installé
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller n'est pas installé. Installation en cours...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer PyInstaller
        popd
        exit /b 1
    )
)

REM Lancer le build
echo.
echo Lancement du build PyInstaller...
python -m PyInstaller build\edupaie.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERREUR: Le build a échoué
    echo ========================================
    popd
    exit /b 1
)

echo.
echo ========================================
echo Build terminé avec succès !
echo ========================================
echo.
echo L'exécutable se trouve dans: dist\EduPaie.exe
echo.

set "ISCC_PATH="
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC_PATH if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if defined ISCC_PATH (
    echo Création de l'installateur Inno Setup...
    "%ISCC_PATH%" "%~dp0edupaie.iss"
    if errorlevel 1 (
        echo ERREUR: La création de l'installateur a échoué
        popd
        exit /b 1
    )
    echo Installateur créé dans: dist\installer\EduPaie-Setup-1.0.1.exe
) else (
    echo AVERTISSEMENT: Inno Setup 6 n'est pas installé.
    echo L'exécutable est prêt, mais l'installateur n'a pas été généré.
    echo Installez Inno Setup 6 puis relancez ce script.
)

popd
