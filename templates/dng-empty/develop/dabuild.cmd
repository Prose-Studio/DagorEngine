@rem dabuild: exports assets\ into the game packs (..\game\content), as the content target of the client tree does
@pushd "%~dp0"
@call ..\_engine.cmd || (echo Configure the project first: cmake --preset ^<host^>-client in prog & popd & exit /b 1)
@"%DAGOR_CDK_DIR%\daBuild-dev.exe" ..\application.blk -q -jobs:%NUMBER_OF_PROCESSORS% %*
@set ERR=%ERRORLEVEL%
@popd
@exit /b %ERR%
