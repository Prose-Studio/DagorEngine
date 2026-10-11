# daScript's standard dialogs (open/save file, message boxes) on the platform's API (replaces the upstream
# CMakeLists.txt of daScript's own build)
# the tray backends are not wired on any platform (as in the jamfile): Dagor hosts no tray icon, and tray_* is bound
# either way, TrayPlatformCreate returning null
set(sources src/dasStdDlg.cpp src/dasStdDlgTray.cpp src/dasStdDlgTrayNotImplemented.cpp)
if(DAGOR_PLATFORM STREQUAL "windows")
  list(APPEND sources src/dasStdDlgWin.cpp)
elseif(DAGOR_PLATFORM STREQUAL "linux")
  list(APPEND sources src/dasStdDlgGtk.cpp)
elseif(DAGOR_PLATFORM STREQUAL "macOS")
  list(APPEND sources src/dasStdDlgOsx.mm)
else()
  list(APPEND sources src/dasStdDlgNotImplemented.cpp)
endif()
dagor_add_library(STRICT
  SOURCES ${sources}
  PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  DEPS 1stPartyLibs/daScript
)
