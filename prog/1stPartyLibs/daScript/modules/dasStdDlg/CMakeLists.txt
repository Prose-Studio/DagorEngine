# daScript's standard dialogs (open/save file, message boxes) on the platform's API (replaces the upstream
# CMakeLists.txt of daScript's own build)
# the tray backends are not wired on any platform: Dagor hosts no tray icon, and tray_* is bound
# either way, TrayPlatformCreate returning null
dagor_add_target(NAME 1stPartyLibs.daScript.modules.dasStdDlg STATIC
  FILES_CMAKE dasStdDlg_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript
)
