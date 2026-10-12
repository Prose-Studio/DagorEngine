# Breakpad's common macOS code: Mach-O readers and ids
dagor_add_library(3rdPartyLibs.breakpad.common.mac LAX file_id.cc macho_id.cc macho_reader.cc macho_utilities.cc
  macho_walker.cc string_utilities.cc arch_utilities.cc)
target_include_directories(3rdPartyLibs.breakpad.common.mac PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
