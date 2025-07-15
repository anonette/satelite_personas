@echo off
echo 🎭 Prague Spectral Theater Launcher
echo ===================================
echo.
echo 🚀 Launching Civic Theater Stage...
echo.

REM Activate virtual environment and launch theater
call spectral_env\Scripts\activate.bat
python -m streamlit run core/theater/civic_theater_stage.py

echo.
echo 👋 Theater session ended. Press any key to exit.
pause > nul
