if(LINUX AND DAGOR_SANITIZE STREQUAL "thread")
  list(APPEND c_options -Wno-tsan -fno-sanitize=thread)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND c_options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.libev STATIC LAX
  FILES_CMAKE libev_files.cmake
  COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H
  COMPILE_OPTIONS PRIVATE "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)
