# IJG libjpeg 6b
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-shift-negative-value)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations -Wno-shift-negative-value)
endif()

dagor_add_target(NAME 3rdPartyLibs.image.jpeg-6b STATIC LAX
  FILES_CMAKE jpeg-6b_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/image/jpeg-6b
  COMPILE_DEFINITIONS PRIVATE NO_GETENV
  COMPILE_OPTIONS PRIVATE ${options}
)
