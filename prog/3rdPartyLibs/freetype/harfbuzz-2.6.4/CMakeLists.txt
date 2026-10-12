set(defines __B_NO_MEM_BASE_INCLUDE _CRT_SECURE_NO_WARNINGS HAVE_FREETYPE HB_NO_GETENV HB_USE_ATEXIT)
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND options -wd4267)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Android|Linux)$")
  list(APPEND defines HAVE_PTHREAD)
endif()

dagor_add_target(NAME 3rdPartyLibs.freetype.harfbuzz-2.6.4 STATIC LAX
  FILES_CMAKE harfbuzz-2.6.4_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/harfbuzz-2.6.4/src
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)
