@ECHO OFF
python test.py

if %ERRORLEVEL% NEQ 0 echo "FAILED TEST"
if %ERRORLEVEL% NEQ 0 exit /b 1