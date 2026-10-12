# dolphin, the lexer generator of the shader compilers' parsers (with whale, see ../whale). jam built it rel only, into
# the source tree; here it is a program of the tree that the parser generation runs, and part of the CDK.
set(options)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND options -funsigned-char)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-potentially-evaluated-expression)
  if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
    list(APPEND options -Wno-deprecated-declarations)
  endif()
  if(LINUX)
    list(APPEND options -Wno-sometimes-uninitialized)
  endif()
endif()

dagor_add_target(NAME dolphin EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE dolphin_files.cmake
  INCLUDE_DIRECTORIES PRIVATE nstl hash
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  COMPILE_OPTIONS PRIVATE ${options}
  PROPERTIES DAGOR_EXCEPTIONS SEH DAGOR_RTTI ON
  CDK
)
