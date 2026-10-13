dagor_add_target(NAME 3rdPartyLibs.fileWatcher STATIC LAX
  FILES_CMAKE fileWatcher_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/fileWatcher/include
)
