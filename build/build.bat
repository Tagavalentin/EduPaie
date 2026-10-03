@echo off
REM Script de build pour EduPaie avec PyInstaller (Windows)

echo ========================================
echo Build EduPaie avec PyInstaller
echo ========================================
echo.

REM Vérifier si PyInstaller est installé
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller n'est pas installé. Installation en cours...
    pip install pyinstaller
)

REM Initialiser la base de données si elle n'existe pas
if not exist "data\edupaie.db" (
    echo Initialisation de la base de données...
    python -m src.database.init_db
)

REM Lancer le build
echo.
echo Lancement du build PyInstaller...
pyinstaller build\edupaie.spec --onefile --windowed

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERREUR: Le build a échoué
    echo ========================================
    exit /b 1
)

echo.
echo ========================================
echo Build terminé avec succès !
echo ========================================
echo.
echo L'exécutable se trouve dans: dist\EduPaie.exe
echo.

pause
