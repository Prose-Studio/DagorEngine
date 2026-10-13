@rem daEditor for this project: its workspace is made from ..\application.blk on the first start
@pushd "%~dp0"
@call ..\_engine.cmd || (echo Configure the project first: cmake --preset ^<host^>-client in prog & popd & exit /b 1)
@start "" "%DAGOR_CDK_DIR%\daEditor3x-dev.exe" ..\application.blk %*
@popd
