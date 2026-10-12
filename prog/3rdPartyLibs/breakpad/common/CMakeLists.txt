# Breakpad's common code: the platform's (windows/, linux/, mac/), and on Linux and macOS the symbol and DWARF readers of
# its tools and client
if(WIN32)
  return()
endif()

dagor_add_target(NAME 3rdPartyLibs.breakpad.common STATIC LAX
  FILES_CMAKE common_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  # StabsReader needs a.out.h (Linux) or mach-o/nlist.h (macOS)
  COMPILE_DEFINITIONS PRIVATE $<IF:$<PLATFORM_ID:Darwin>,HAVE_MACH_O_NLIST_H,HAVE_A_OUT_H>
  COMPILE_OPTIONS PRIVATE -Wno-unused-parameter "$<$<PLATFORM_ID:Darwin>:-Wno-deprecated-declarations>"
)
