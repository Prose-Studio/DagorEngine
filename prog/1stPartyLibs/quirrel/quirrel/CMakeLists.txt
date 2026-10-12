# Quirrel: the VM and its standard library (the engine's build replaces upstream's CMakeLists.txt; the compiler is
# squirrel/compiler, the module system sqmodules)
set(defines SQ_EXCLUDE_DEFAULT_MEMFUNCTIONS
  "$<IF:$<CONFIG:Rel,IRel>,SQ_RUNTIME_TYPE_CHECK=0;SQ_STACK_DUMP_SECRET_PREFIX=no_dump_,SQ_CHECK_THREAD;SQ_RANDOMIZE_FOREACH=1>")
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
if(NOT CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux|Windows)$")
  list(APPEND defines SQ_SYSTEM_STUBS=1)
endif()

dagor_add_target(NAME 1stPartyLibs.quirrel.quirrel STATIC LAX
  FILES_CMAKE quirrel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE squirrel internal helpers
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE Dagor::QuirrelHeaders 3rdPartyLibs.eastl 1stPartyLibs.quirrel.quirrel.squirrel.compiler
  LICENSES COPYRIGHT
)
