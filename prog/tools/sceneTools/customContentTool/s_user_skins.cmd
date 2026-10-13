@echo off
call ..\..\..\..\prog\tools\make_dagor_tools_path.cmd
for /D %%D in (userSkins/*) do (
  echo ---- %%D
  for %%f in ("userSkins/%%~D/*.blk") do %DAGOR_CDK_DIR%\customContentTool-dev cfg_user_skin.blk "%%~D" "userSkins/%%~D/%%~f"
)
