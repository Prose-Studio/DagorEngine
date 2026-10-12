# FreeType 2.8 (the modules of the engine's font rendering; no bzip2/gzip/lzw streams)
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND options /wd4267) # conversion from 'size_t' to 'int', possible loss of data
elseif(NOT MSVC)
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.freetype.freetype-2.8 STATIC LAX
  FILES_CMAKE freetype-2.8_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include src
  COMPILE_DEFINITIONS PRIVATE FT2_BUILD_LIBRARY
  COMPILE_OPTIONS PRIVATE ${options}
)
