# PCRE 8.31 (classic PCRE1) with the JIT compiler and the C++ wrapper; per-platform generated character tables
if(WIN32)
  set(includes win32)
elseif(ANDROID)
  set(includes linux32)
elseif(LINUX)
  set(includes linux64)
elseif(APPLE)
  set(includes macosx)
endif()
list(APPEND includes pcre)
set(c_options -DHAVE_CONFIG_H)
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.pcre STATIC LAX
  FILES_CMAKE pcre_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
