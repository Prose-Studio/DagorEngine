# Breakpad's common Linux code: ELF symbols and ids, memory-mapped files, the C library helpers of its client
dagor_add_target(NAME 3rdPartyLibs.breakpad.common.linux STATIC LAX
  FILES_CMAKE linux_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  COMPILE_OPTIONS PRIVATE -Wno-unused-parameter
)
