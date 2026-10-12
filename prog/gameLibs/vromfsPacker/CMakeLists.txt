# The vromfs pack builder: file selection by patterns, BLK and text preprocessing, packing
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/tools/sharedInclude)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)
list(APPEND deps 3rdPartyLibs.openssl-3.x)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps engine.osApiWrappers engine.ioSys engine.baseUtil)
endif()
list(APPEND deps tools.libTools.util 3rdPartyLibs.hash.BLAKE3)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-deprecated-declarations)
endif()

dagor_add_target(NAME gameLibs.vromfsPacker STATIC
  FILES_CMAKE vromfsPacker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
