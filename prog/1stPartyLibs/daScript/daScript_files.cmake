# project_specific_file_info.cpp provides fallbacks of get_file_access / get_context / get_clone_context that every
# Dagor program supplies itself (games through das_es.cpp + defaultFileAccess.cpp, tools through dagorAdapter/da.cpp),
# and src/hal/performance_time.cpp the time functions the engine kernel provides: they would be duplicate symbols
dagor_glob_sources(FILES DIRS src/ast src/builtin src/runtime src/simulate src/misc src/parser src/modules/uriparser
  src/hal GLOB *.cpp EXCLUDE "project_specific_file_info\\.cpp$" "performance_time\\.cpp$")
list(APPEND FILES dagorAdapter/das_jit_runtime.cpp) # (empty without DAS_JIT_RUNTIME)

# the sources that throw (and the crash handler, which reads the exception in flight): compiled with exceptions
# whatever the tree's setting
if(MSVC)
  set(exceptions /EHsc -D_HAS_EXCEPTIONS=1 -DDAS_ENABLE_EXCEPTIONS)
else()
  set(exceptions -fexceptions -DDAS_ENABLE_EXCEPTIONS)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND exceptions -Wno-macro-redefined)
endif()
foreach(file IN LISTS FILES)
  if(file MATCHES "(_exceptions|_ast_serialize|runtime_string|format|crash_handler)\\.cpp$")
    set_property(SOURCE "${file}" PROPERTY COMPILE_OPTIONS ${exceptions})
  endif()
endforeach()
if(DAGOR_ARCH STREQUAL "e2k")
  set_property(SOURCE src/simulate/simulate_gc.cpp PROPERTY COMPILE_OPTIONS -Wno-overloaded-virtual)
endif()
