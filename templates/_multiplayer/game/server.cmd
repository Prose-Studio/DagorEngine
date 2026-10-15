@rem Runs the dedicated server on port 2992 (clients join with client.cmd -connect:localhost); scripts are read from ..\prog
@pushd "%~dp0"
@set ARCH=x86_64
@if "%PROCESSOR_ARCHITECTURE%" == "ARM64" set ARCH=arm64
@windows-%ARCH%\starter_game-ded-dev.exe -config:debug/useAddonVromSrc:b=yes -listen:0.0.0.0:2992 %*
@set ERR=%ERRORLEVEL%
@popd
@exit /b %ERR%
