# The Quirrel compiler and static analyzer, which report errors with C++ exceptions: they are on for its code whatever
# the tree's exception settings (as jam did); the engine's build replaces upstream's CMakeLists.txt
set(defines)
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
set(options -fexceptions)
if(MSVC)
  set(options /EHsc)
endif()
dagor_add_target(NAME 1stPartyLibs.quirrel.quirrel.squirrel.compiler STATIC LAX
  FILES_CMAKE compiler_files.cmake
  INCLUDE_DIRECTORIES PRIVATE .. . ../../helpers ../../internal
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::QuirrelHeaders 3rdPartyLibs.eastl
)
