# The Quirrel command-line interpreter as a library: sq_interpreter_main() for a program's main, and the test.native
# module of the interpreter's tests. The engine's build replaces upstream's CMakeLists.txt.
set(defines SQ_EXCLUDE_DEFAULT_MAIN)
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
dagor_add_target(NAME 1stPartyLibs.quirrel.quirrel.sq STATIC LAX
  FILES_CMAKE sq_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ../sqmodules ../squirrel
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PUBLIC Dagor::Quirrel
)
