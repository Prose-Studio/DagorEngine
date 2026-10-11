# The Quirrel compiler and static analyzer, which report errors with C++ exceptions: they are on for its code whatever
# the tree's exception settings (as jam did); the engine's build replaces upstream's CMakeLists.txt
set(defines)
if(DAGOR_SQ_VAR_TRACE)
  list(APPEND defines SQ_VAR_TRACE_ENABLED)
endif()
set(options -fexceptions)
if(DAGOR_MSVC_LIKE)
  set(options /EHsc)
endif()
dagor_add_library(QUIRREL_HEADERS
  SOURCES
    ast.cpp
    compilationcontext.cpp
    parser.cpp
    codegen.cpp
    typeinference.cpp
    constgen.cpp
    compiler.cpp
    sqfuncstate.cpp
    sqdump.cpp
    optimizer.cpp
    lexer.cpp
    sqtypeparser.cpp
    optimizations/closureHoisting.cpp
    static_analyzer/analyzer.cpp
    static_analyzer/checker_visitor.cpp
    static_analyzer/name_shadowing_checker.cpp
    static_analyzer/function_ret_type_eval.cpp
    static_analyzer/config.cpp
    static_analyzer/var_scope.cpp
    static_analyzer/value_ref.cpp
    static_analyzer/naming.cpp
    static_analyzer/global_state.cpp
    static_analyzer/external_value.cpp
  PRIVATE_INCLUDES .. . ../../helpers ../../internal
  PRIVATE_DEFINES ${defines}
  COMPILE_OPTIONS ${options}
  DEPS 3rdPartyLibs/eastl
)
