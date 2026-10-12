# libzip: reading, creating and modifying zip archives (on zlib-ng, with WinZip AES encryption)
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.arc.libzip STATIC LAX
  FILES_CMAKE libzip_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/libzip ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/libzip/lib
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/libzip/lib/gladman-fcrypt ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_DEFINITIONS PRIVATE ZIP_STATIC
  COMPILE_OPTIONS PRIVATE ${options}
)
