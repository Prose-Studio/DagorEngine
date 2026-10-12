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
dagor_add_library(1stPartyLibs.quirrel.quirrel.squirrel.compiler LAX ast.cpp compilationcontext.cpp parser.cpp
  codegen.cpp typeinference.cpp constgen.cpp compiler.cpp sqfuncstate.cpp sqdump.cpp optimizer.cpp lexer.cpp
  sqtypeparser.cpp optimizations/closureHoisting.cpp static_analyzer/analyzer.cpp static_analyzer/checker_visitor.cpp
  static_analyzer/name_shadowing_checker.cpp static_analyzer/function_ret_type_eval.cpp static_analyzer/config.cpp
  static_analyzer/var_scope.cpp static_analyzer/value_ref.cpp static_analyzer/naming.cpp
  static_analyzer/global_state.cpp static_analyzer/external_value.cpp)
target_include_directories(1stPartyLibs.quirrel.quirrel.squirrel.compiler PRIVATE .. . ../../helpers ../../internal)
target_compile_definitions(1stPartyLibs.quirrel.quirrel.squirrel.compiler PRIVATE ${defines})
target_compile_options(1stPartyLibs.quirrel.quirrel.squirrel.compiler PRIVATE ${options})
target_link_libraries(1stPartyLibs.quirrel.quirrel.squirrel.compiler PRIVATE Dagor::QuirrelHeaders 3rdPartyLibs.eastl)
