@echo off
python -m venv venv
CALL venv\Scripts\activate.bat
pip install -r requirements.txt
echo Setup complete.
pause