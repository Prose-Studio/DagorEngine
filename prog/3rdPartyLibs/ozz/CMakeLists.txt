if(LINUX)
  list(APPEND options -Wno-error=uninitialized)
endif()

dagor_add_target(NAME 3rdPartyLibs.ozz STATIC LAX
  FILES_CMAKE ozz_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include src
  COMPILE_OPTIONS PRIVATE ${options}
)
