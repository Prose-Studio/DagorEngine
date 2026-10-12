# daScript's standard dialogs module where there are none: the sources are in the parent dir
dagor_add_target(NAME 1stPartyLibs.daScript.modules.dasStdDlg.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript
)
