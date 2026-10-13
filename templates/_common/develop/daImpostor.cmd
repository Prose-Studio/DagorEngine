@rem impostorBaker: bakes impostor textures of the assets that use them
@pushd "%~dp0"
@call ..\_engine.cmd || (echo Configure the project first: cmake --preset ^<host^>-client in prog & popd & exit /b 1)
@"%DAGOR_CDK_DIR%\impostorBaker-dev.exe" ..\application.blk -rootdir:./ -clean:yes %*
@set ERR=%ERRORLEVEL%
@popd
@exit /b %ERR%
