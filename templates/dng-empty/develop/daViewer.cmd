@rem daViewer (assetViewer) for the assets in assets\
@pushd "%~dp0"
@call ..\_engine.cmd || (echo Configure the project first: cmake --preset ^<host^>-client in prog & popd & exit /b 1)
@start "" "%DAGOR_CDK_DIR%\assetViewer2-dev.exe" ..\application.blk %*
@popd
