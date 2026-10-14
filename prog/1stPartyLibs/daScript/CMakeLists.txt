# daScript: the compiler, runtime and builtin modules. Two builds, linked by the choice of each program:
#   1stPartyLibs.daScript.standard  log output through the engine
#   1stPartyLibs.daScript.console   stdout output and daScript's own crash handler, for the console tools (the das
#                                   interpreter) that set the DAGOR_DAS_CONSOLE target property
# Libraries depend on 1stPartyLibs/daScript, which links the one of the program they end up in. The two differ in 4
# sources (daScript_build_files.cmake): the others are compiled once, into 1stPartyLibs.daScript.common.
# DAS_ENABLE_DYN_INCLUDES: as daScript's own CMake build defines it (src/builtin/jit_runtime.cpp needs its header)
set(defines DAS_ENABLE_KEEPALIVE=0 FMT_UNICODE=0 DAS_ENABLE_DYN_INCLUDES=1 "$<$<CONFIG:Rel,IRel>:DAS_NO_ASSERTIONS=1>")
if(DAGOR_DAS_LLVM_AOT)
  list(APPEND defines DAS_LLVM_AOT)
endif()
set(options)
if(NOT MSVC)
  # the language's floats are IEEE: its comparisons and isnan/isinf see NaN and infinity (-ffinite-math-only would let
  # the compiler assume them away, and arm64 code then answers wrongly)
  list(APPEND options -fno-finite-math-only)
  if(DAGOR_FP_MODEL STREQUAL "fast")
    # which drops __FAST_MATH__ while -ffast-math's reciprocal math stays: say so (platform.h, HOST_FAST_MATH)
    list(APPEND defines DAS_FAST_INTEGER_MOD=0)
  endif()
endif()
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  list(APPEND options -Wno-stringop-overflow)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
endif()

set(aot_deps)
if(DAGOR_DAS_AOT)
  set(aot_deps 1stPartyLibs.daScript.daslib) # daslib's scripts compiled ahead of time
endif()
set(includes include include/das_hash_map include/modules/uriparser ${DAGOR_PROG_DIR}/3rdPartyLibs/uriparser/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/fmt/include)
set(deps 3rdPartyLibs.eastl 3rdPartyLibs.uriparser 3rdPartyLibs.fmt ${aot_deps})
# what both builds share, compiled once (an object library: its objects go into each build's library)
dagor_add_target(NAME 1stPartyLibs.daScript.common OBJECT LAX
  FILES_CMAKE daScript_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
foreach(build standard console)
  set(build_defines ${defines})
  if(build STREQUAL "console")
    list(APPEND build_defines DAS_DEFAULT_STDOUT DAS_USE_BASE_CRASH_HANDLER=1)
  endif()
  dagor_add_target(NAME 1stPartyLibs.daScript.${build} STATIC LAX
    FILES_CMAKE daScript_build_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${includes}
    COMPILE_DEFINITIONS PRIVATE ${build_defines}
    COMPILE_OPTIONS PRIVATE ${options}
    BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript.common ${deps}
    LICENSES LICENSE
  )
endforeach()
dagor_add_link_choice(1stPartyLibs.daScript PROPERTY DAGOR_DAS_CONSOLE
  ON 1stPartyLibs.daScript.console OFF 1stPartyLibs.daScript.standard)

# the daScript language and daslib test suite, run by the engine's das interpreter (dastest/tests is not included: it
# spawns '<exe> dastest.das' the way the standalone daslang host is invoked); the tests of daScript's tools and of the
# daslive sample's game logic, from the daScript root (their fixtures are root-relative)
if(DAGOR_ENGINE_TESTS)
  dagor_add_das_test(daScript.suite PATHS tests TAGS daScript TIMEOUT 1800)
  foreach(tool lint gen1-to-gen2 find-dupe dascov common)
    dagor_add_das_test(daScript.utils.${tool} PATHS utils/${tool}/tests WORKING_DIRECTORY . TAGS daScript)
  endforeach()
  foreach(tool hygiene requirefix detect-dupe)
    string(REPLACE "-" "_" file ${tool})
    dagor_add_das_test(daScript.utils.${tool} PATHS utils/${tool}/test_${file}.das WORKING_DIRECTORY . TAGS daScript)
  endforeach()
  set(sequence examples/daslive/sequence)
  dagor_add_das_test(daScript.daslive.sequence WORKING_DIRECTORY . TAGS daScript
    PATHS ${sequence}/test_anim.das ${sequence}/test_bots.das ${sequence}/test_gameplay.das)
endif()
