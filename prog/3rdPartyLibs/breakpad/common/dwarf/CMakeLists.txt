# Breakpad's DWARF readers (its dump_syms tools), which use dynamic_cast
dagor_add_target(NAME 3rdPartyLibs.breakpad.common.dwarf STATIC LAX
  FILES_CMAKE dwarf_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  COMPILE_OPTIONS PRIVATE -Wno-unused-parameter
  PROPERTIES DAGOR_RTTI ON
)
