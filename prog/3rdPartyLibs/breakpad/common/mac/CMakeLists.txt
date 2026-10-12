# Breakpad's common macOS code: Mach-O readers and ids
dagor_add_target(NAME 3rdPartyLibs.breakpad.common.mac STATIC LAX
  FILES_CMAKE mac_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
)
