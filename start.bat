@ECHO OFF
echo %time%
FOR /F %%i IN (ascii.txt) DO @echo %%i
echo "Starting Application..."
if not exist venv\ (
  echo "Setting up python virtual environment."
  "py" "-m" "ensurepip" "--upgrade"
  "py" "-m" "venv" "venv"
  "%cd%\venv\Scripts\activate.bat"
  "pip" "install" "-r" "requirements.txt"
  echo "App set up!"
  pause
  %0
) else ( 
  echo "Environment detect as already set up (venv)"
)
timeout 2 > NUL
START /MIN CMD.EXE /C app.bat
echo "Application started in background."
echo "Please validate by checking the Task Manager for a pythonw process running the twitter webscraper."
echo "Make sure the config.txt values are correct!"
echo "If they're wrong, run stop.bat and edit the config.txt file!"
pause