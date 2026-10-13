# breakpad's dump_syms: the symbol files of programs for the crash reports (tools/util)
dagor_add_target(NAME dump_syms EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE dump_syms_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.breakpad.common 3rdPartyLibs.breakpad.common.mac 3rdPartyLibs.breakpad.common.dwarf
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  PROPERTIES DAGOR_EXCEPTIONS SEH DAGOR_RTTI ON
)
