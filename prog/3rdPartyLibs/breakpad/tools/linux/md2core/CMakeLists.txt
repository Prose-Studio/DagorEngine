# breakpad's minidump-2-core: a core file of a minidump (tools/util)
dagor_add_target(NAME minidump-2-core EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE md2core_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.breakpad.common.linux
  LICENSES ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad
)
