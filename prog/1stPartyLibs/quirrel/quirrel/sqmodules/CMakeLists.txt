# Quirrel's module system (require(), file access); the engine's build replaces upstream's CMakeLists.txt
set(options)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND options -wd4267)
endif()
dagor_add_target(NAME 1stPartyLibs.quirrel.quirrel.sqmodules STATIC LAX
  FILES_CMAKE sqmodules_files.cmake
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::QuirrelHeaders
)
