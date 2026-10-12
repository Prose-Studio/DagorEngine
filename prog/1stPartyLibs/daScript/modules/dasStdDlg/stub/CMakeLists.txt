# daScript's standard dialogs module where there are none: the sources are in the parent dir
dagor_add_library(1stPartyLibs.daScript.modules.dasStdDlg.stub ../src/dasStdDlg.cpp ../src/dasStdDlgNotImplemented.cpp
  ../src/dasStdDlgTray.cpp ../src/dasStdDlgTrayNotImplemented.cpp)
target_include_directories(1stPartyLibs.daScript.modules.dasStdDlg.stub PRIVATE
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
target_link_libraries(1stPartyLibs.daScript.modules.dasStdDlg.stub PRIVATE 1stPartyLibs.daScript)
