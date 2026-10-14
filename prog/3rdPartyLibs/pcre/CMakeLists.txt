# PCRE 8.31 (classic PCRE1) with the JIT compiler and the C++ wrapper; per-platform generated character tables
if(WIN32)
  set(includes win32)
elseif(ANDROID)
  set(includes linux32)
elseif(LINUX)
  set(includes linux64)
elseif(APPLE)
  set(includes macosx)
endif()
list(APPEND includes pcre)
set(c_options -DHAVE_CONFIG_H)
if(CMAKE_CXX_COMPILER_ID MATCHES "^(Clang|AppleClang|GNU)$")
  list(APPEND options -Wno-unused-parameter)
endif()

dagor_add_target(NAME 3rdPartyLibs.pcre STATIC LAX
  FILES_CMAKE pcre_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H
  COMPILE_OPTIONS PRIVATE ${options} "$<$<COMPILE_LANGUAGE:C>:${c_options}>"
)

# PCRE's own tests of its C++ wrapper (pcrecpp, its scanner and StringPiece), on the engine's build of it (with the
# engine's runtime, which the forced dag_memBase.h needs; they format with sprintf, which the macOS SDK deprecates)
if(DAGOR_ENGINE_TESTS)
  set(test_options ${options})
  if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    list(APPEND test_options -Wno-deprecated-declarations)
  endif()
  foreach(test pcrecpp_unittest pcre_scanner_unittest pcre_stringpiece_unittest)
    dagor_add_target(NAME pcre-${test} EXECUTABLE LAX
      FILES_CMAKE unittest_files.cmake
      INCLUDE_DIRECTORIES PRIVATE ${includes}
      COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H
      COMPILE_OPTIONS PRIVATE ${test_options}
      BUILD_DEPENDENCIES PRIVATE
        3rdPartyLibs.pcre engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.perfMon.daProfilerStub
        3rdPartyLibs.eastl
    )
    dagor_add_exec_test(3rdPartyLibs.pcre.${test} COMMAND $<TARGET_FILE:pcre-${test}> TAGS 3rdPartyLibs)
  endforeach()
endif()
