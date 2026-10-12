# Breakpad's common code: the platform's (windows/, linux/, mac/), and on Linux and macOS the symbol and DWARF readers of
# its tools and client
if(WIN32)
  add_subdirectory(windows)
  return()
elseif(APPLE)
  add_subdirectory(mac)
else()
  add_subdirectory(linux)
endif()
add_subdirectory(dwarf)

dagor_add_library(3rdPartyLibs.breakpad.common LAX dwarf_cfi_to_module.cc dwarf_cu_to_module.cc dwarf_line_to_module.cc
  language.cc module.cc stabs_reader.cc stabs_to_module.cc string_conversion.cc convert_UTF.c simple_string_dictionary.cc
  md5.cc)
target_include_directories(3rdPartyLibs.breakpad.common PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
# StabsReader needs a.out.h (Linux) or mach-o/nlist.h (macOS)
target_compile_definitions(3rdPartyLibs.breakpad.common PRIVATE $<IF:$<PLATFORM_ID:Darwin>,HAVE_MACH_O_NLIST_H,HAVE_A_OUT_H>)
target_compile_options(3rdPartyLibs.breakpad.common PRIVATE -Wno-unused-parameter
  "$<$<PLATFORM_ID:Darwin>:-Wno-deprecated-declarations>")
