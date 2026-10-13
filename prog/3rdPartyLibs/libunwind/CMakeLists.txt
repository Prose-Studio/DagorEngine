# libunwind for the Android arm64 crash stacks
dagor_add_target(NAME 3rdPartyLibs.libunwind STATIC LAX
  FILES_CMAKE libunwind_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/include/tdep-aarch64
    ${DAGOR_PROG_DIR}/3rdPartyLibs/libunwind/src
  COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H __EXTENSIONS__ _GNU_SOURCE NDEBUG
)
