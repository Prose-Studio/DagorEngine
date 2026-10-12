# daScript's standard dialogs (open/save file, message boxes) on the platform's API (replaces the upstream
# CMakeLists.txt of daScript's own build)
# the tray backends are not wired on any platform (as in the jamfile): Dagor hosts no tray icon, and tray_* is bound
# either way, TrayPlatformCreate returning null
add_subdirectory(stub)

set(sources src/dasStdDlg.cpp src/dasStdDlgTray.cpp src/dasStdDlgTrayNotImplemented.cpp)
if(WIN32)
  list(APPEND sources src/dasStdDlgWin.cpp)
elseif(LINUX)
  list(APPEND sources src/dasStdDlgGtk.cpp)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND sources src/dasStdDlgOsx.mm)
else()
  list(APPEND sources src/dasStdDlgNotImplemented.cpp)
endif()
dagor_add_library(1stPartyLibs.daScript.modules.dasStdDlg ${sources})
target_include_directories(1stPartyLibs.daScript.modules.dasStdDlg PRIVATE
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
target_link_libraries(1stPartyLibs.daScript.modules.dasStdDlg PRIVATE 1stPartyLibs.daScript)
