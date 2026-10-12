# libpng 1.4.22 (on zlib-ng)
if(DAGOR_ARCH STREQUAL "x86_64" AND WIN32)
  list(APPEND c_options /wd4267)
endif()

dagor_add_target(NAME 3rdPartyLibs.image.libpng-1.4.22 STATIC LAX
  FILES_CMAKE libpng-1.4.22_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_DEFINITIONS PRIVATE PNG_NO_CONSOLE_IO PNG_NO_WRITE_FLUSH
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
