@rem daViewer (assetViewer) for the assets in assets\
@pushd "%~dp0"
@call ..\_engine.cmd || (echo Set the project up first: python3 prog\build.py & popd & exit /b 1)
@start "" "%DAGOR_CDK_DIR%\assetViewer2-dev.exe" ..\application.blk %*
@popd
