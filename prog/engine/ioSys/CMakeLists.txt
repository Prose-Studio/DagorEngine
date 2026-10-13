# Streams (files, memory, zlib, zstd, lzma, brotli, Oodle), async I/O, vromfs, findFiles. Oodle is not redistributable:
# with -DOodle_ROOT=<oodle SDK> its codecs are built in, otherwise a stub reports them unsupported.
set(deps engine.ioSys.dataBlock 3rdPartyLibs.hash 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.arc.zstd-1.4.5
  3rdPartyLibs.arc.lzma-9.20 3rdPartyLibs.arc.brotli)
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  list(APPEND deps 3rdPartyLibs.eastl)
endif()

find_package(Oodle)
if(Oodle_FOUND)
  list(APPEND deps Oodle::Oodle)
endif()

dagor_add_target(NAME engine.ioSys STATIC
  FILES_CMAKE ioSys_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/brotli/include
  COMPILE_DEFINITIONS PRIVATE __B_KERNEL_LIB USE_ZLIB_VER=0xFF0000
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
