@echo off
REM ========================================================================
REM  Supply Chain Mapping - Daily Update Script (Windows)
REM ========================================================================
REM
REM  One-time setup:
REM    1. Right-click this file and select "Edit"
REM    2. Find the line that says: set API_KEY=YOUR_API_KEY_HERE
REM    3. Replace YOUR_API_KEY_HERE with your actual Anthropic API key
REM    4. Save and close
REM
REM  Daily use:
REM    Just double-click this file!
REM
REM ========================================================================

echo.
echo ================================================
echo    SUPPLY CHAIN MAPPING - DAILY UPDATE
echo ================================================
echo.

REM ========================================================================
REM CONFIGURATION - EDIT THIS SECTION
REM ========================================================================

REM TODO: Replace YOUR_API_KEY_HERE with your actual API key from console.anthropic.com
set API_KEY= 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

REM Project folder (update if different)
set PROJECT_DIR=C:\Users\jalex\supply-chain\supply-chain-mapping

REM ========================================================================
REM NO NEED TO EDIT BELOW THIS LINE
REM ========================================================================

REM Check if API key is set
if "%API_KEY%"=="YOUR_API_KEY_HERE" (
    echo ERROR: API key not configured!
    echo.
    echo Please edit this file and replace YOUR_API_KEY_HERE with your actual API key.
    echo.
    echo How to edit:
    echo   1. Right-click this file
    echo   2. Select "Edit"
    echo   3. Find line 22: set API_KEY=YOUR_API_KEY_HERE
    echo   4. Replace YOUR_API_KEY_HERE with your key from console.anthropic.com
    echo   5. Save and close
    echo.
    pause
    exit /b 1
)

REM Navigate to project directory
cd /d "%PROJECT_DIR%"

if not exist "orchestrator.py" (
    echo ERROR: Cannot find orchestrator.py
    echo.
    echo Make sure you're in the right directory: %PROJECT_DIR%
    echo.
    pause
    exit /b 1
)

REM Run daily update
echo Starting daily update...
echo.

python orchestrator.py --api-key %API_KEY% daily

REM Check if it ran successfully
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo    Update complete!
    echo ================================================
    echo.
) else (
    echo.
    echo ================================================
    echo    ERROR: Update failed!
    echo ================================================
    echo.
    echo Check the error message above.
    echo.
)

REM Check for items needing review
echo Checking for items needing your review...
echo.
python orchestrator.py --api-key %API_KEY% review

echo.
echo Press any key to close this window...
pause > nul
