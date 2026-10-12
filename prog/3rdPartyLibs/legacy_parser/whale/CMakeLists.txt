# whale, the LR parser generator of the shader compilers' parsers (with dolphin, see ../dolphin). jam built it rel only,
# into the source tree; here it is a program of the tree that the parser generation runs.
set(options)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND options -funsigned-char)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-potentially-evaluated-expression)
  if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
    list(APPEND options -Wno-logical-op-parentheses -Wno-dangling-else)
  endif()
  if(LINUX)
    list(APPEND options -Wno-deprecated-declarations -Wno-sometimes-uninitialized)
  endif()
endif()

dagor_add_target(NAME whale EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE whale_files.cmake
  INCLUDE_DIRECTORIES PRIVATE nstl hash
  COMPILE_DEFINITIONS PRIVATE NO_PCRE LR0_SUPPRESS_PROFILING __B_NO_MEM_BASE_INCLUDE
  COMPILE_OPTIONS PRIVATE ${options}
  PROPERTIES DAGOR_EXCEPTIONS SEH DAGOR_RTTI ON
  CDK
)
