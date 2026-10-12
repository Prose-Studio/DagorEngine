# libtiff 4.4.0: TIFF image reading and writing (JPEG through jpeg-6b, deflate through zlib-ng)
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-format-extra-args)
endif()
if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Android|Darwin|Linux|Windows)$")
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND c_options -include stdlib_stub.h)
  endif()
endif()

dagor_add_target(NAME 3rdPartyLibs.image.tiff-4.4.0 STATIC LAX
  FILES_CMAKE tiff-4.4.0_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/image/tiff-4.4.0 ${DAGOR_PROG_DIR}/3rdPartyLibs/image/jpeg-6b
    ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.image.jpeg-6b 3rdPartyLibs.arc.zlib-ng
)
