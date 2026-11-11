@ECHO OFF
pushd %~dp0
if "%SPHINXBUILD%" == "" set SPHINXBUILD=uv run --no-sync sphinx-build
if "%SPHINXOPTS%" == "" set SPHINXOPTS=-W --keep-going
if "%1" == "" goto help
%SPHINXBUILD% -M %1 . _build %SPHINXOPTS% %O%
goto end
:help
%SPHINXBUILD% -M help . _build %SPHINXOPTS% %O%
:end
set BUILD_EXIT_CODE=%ERRORLEVEL%
popd
exit /b %BUILD_EXIT_CODE%
