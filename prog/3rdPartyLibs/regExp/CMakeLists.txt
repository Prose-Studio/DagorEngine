# Regular expressions (Henry Spencer's)
if(APPLE)
  set(options -Wno-unused)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND FALSE)
  set(options -Wno-unused)
endif()
if(WIN32 AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-unused-value)
endif()

dagor_add_target(NAME 3rdPartyLibs.regExp STATIC LAX
  FILES_CMAKE regExp_files.cmake
  COMPILE_OPTIONS PRIVATE ${options}
)
