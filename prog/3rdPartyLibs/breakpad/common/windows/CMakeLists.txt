# Breakpad's common Windows code (string and GUID utilities) for its client
dagor_add_target(NAME 3rdPartyLibs.breakpad.common.windows STATIC LAX
  FILES_CMAKE windows_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
)
