@echo off
REM Daily Reminders Display for Supply Chain Mapping Project

color 0A
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  DAILY REMINDERS                             ║
echo ║           Supply Chain Mapping Project                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🌅 BEFORE YOU START:
echo    [1] Read last entry in PROJECT_STATE.md
echo    [2] Create session_notes.txt for today
echo.
echo 💼 WHILE WORKING:
echo    [1] Keep session_notes.txt updated
echo    [2] Note problems and solutions
echo.
echo 🌆 BEFORE YOU FINISH (if made significant changes):
echo    [1] Update PROJECT_STATE.md
echo        - Change "Last Updated" date
echo        - Add "Completed Today" bullets
echo        - Update data counts
echo    [2] Commit to GitHub
echo        - Open GitHub Desktop
echo        - Write good commit message
echo        - Push to origin
echo    [3] Delete session_notes.txt
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if it's Friday
for /f "tokens=1 delims= " %%a in ('echo %date:~0,3%') do set DAY=%%a
if /i "%DAY%"=="Fri" (
    echo ⚠️  IT'S FRIDAY! Weekly tasks:
    echo    [1] Update README.md metrics
    echo    [2] Backup supply_chain.db
    echo    [3] Commit weekly progress
    echo.
)

REM Check if it's the first few days of the month
for /f "tokens=2 delims=/ " %%a in ('date /t') do set DAY_NUM=%%a
if "%DAY_NUM%"=="01" (
    echo ⚠️  FIRST OF MONTH! Monthly tasks:
    echo    [1] Run monthly audit
    echo    [2] Full backup (db + tariff_library)
    echo    [3] Review documentation
    echo    [4] Check API costs
    echo.
)
if "%DAY_NUM%"=="02" (
    echo ⚠️  MONTHLY TASKS DUE!
    echo    Did you do monthly maintenance yesterday?
    echo.
)
if "%DAY_NUM%"=="03" (
    echo ⚠️  MONTHLY TASKS OVERDUE!
    echo    See REMINDERS.md for monthly checklist!
    echo.
)

echo ═══════════════════════════════════════════════════════════════
echo.
echo 📋 See REMINDERS.md for complete checklist
echo 📋 Print DAILY_CHECKLIST.txt for daily tracking
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo Press any key to continue to main menu...
pause > nul

REM You can add a call to your main menu or script here
REM call main_menu.bat
