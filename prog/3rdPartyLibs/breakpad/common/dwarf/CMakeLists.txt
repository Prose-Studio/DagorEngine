# Breakpad's DWARF readers (its dump_syms tools), which use dynamic_cast
dagor_add_library(3rdPartyLibs.breakpad.common.dwarf LAX bytereader.cc dwarf2diehandler.cc dwarf2reader.cc)
target_include_directories(3rdPartyLibs.breakpad.common.dwarf PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
target_compile_options(3rdPartyLibs.breakpad.common.dwarf PRIVATE -Wno-unused-parameter)
set_target_properties(3rdPartyLibs.breakpad.common.dwarf PROPERTIES DAGOR_RTTI ON)
