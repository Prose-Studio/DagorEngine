set(includes include)
list(APPEND c_options -DHAVE_CONFIG_H)
if(WIN32)
  list(APPEND includes win32)
  list(APPEND c_options /wd4267)
else()
  list(APPEND includes ${CMAKE_CURRENT_SOURCE_DIR})
endif()
if(WIN32)
  list(APPEND c_options -FI../speex_mangle.h)
elseif(CMAKE_SYSTEM_NAME MATCHES "^(Android|iOS|Linux|Darwin)$")
  list(APPEND c_options -include ../speex_mangle.h)
endif()
if(CMAKE_SYSTEM_NAME MATCHES "^(Linux|Darwin)$" AND DAGOR_ARCH STREQUAL "x86_64")
  list(APPEND c_options -DUSE_SSE -DUSE_SSE2)
endif()
if(DAGOR_ARCH STREQUAL "arm64")
  list(APPEND c_options -DUSE_NEON)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.codecs.speexdsp-1.2.0 STATIC LAX
  FILES_CMAKE speexdsp-1.2.0_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
