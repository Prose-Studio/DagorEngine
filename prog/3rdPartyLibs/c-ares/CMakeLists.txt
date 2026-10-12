# c-ares asynchronous DNS resolver
set(c_options -DCARES_STATICLIB)
if(NOT WIN32)
  list(APPEND c_options -DHAVE_CONFIG_H)
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND c_options -Wno-deprecated-declarations)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND c_options -Wno-incompatible-pointer-types-discards-qualifiers)
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND c_options -Wno-unused-result -Wno-discarded-qualifiers)
endif()

dagor_add_target(NAME 3rdPartyLibs.c-ares STATIC LAX
  FILES_CMAKE c-ares_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
