# fmt {fmt} formatting (the engine's build replaces upstream's CMakeLists.txt)
list(APPEND defines FMT_UNICODE=0)
if(WIN32)
  list(APPEND defines _HAS_EXCEPTIONS=1)
  list(APPEND options /EHsc)
else()
  list(APPEND options -fexceptions)
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  list(APPEND options -Wno-macro-redefined)
endif()

dagor_add_target(NAME 3rdPartyLibs.fmt STATIC LAX
  FILES_CMAKE fmt_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
)
