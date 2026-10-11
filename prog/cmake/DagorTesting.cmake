# Tests, run by CTest (python dng.py test, python project.py test). Each test gets the CTest labels of its layer (cpp,
# das, exec, ecs, scenario), its TAGS and its REQUIRES as requires-<what>, so a run selects with -L / -LE: CI excludes
# requires-gpu|requires-display.
#
#   dagor_add_catch2_test(<name> ...)  a Catch2 program (main from <unittest/mainCatch2.inc.cpp>); each test case is
#                                      a CTest test named <name>:<case>
#   dagor_add_das_test(<name> ...)     daScript [test] functions run by dastest on the das interpreter
#   dagor_add_exec_test(<name> ...)    any command; its exit code is the result
#   dagor_add_game_test(<name> ...)    [ecs_test] functions run by the game of the tree in its test mode
#
# The target tests builds the programs the tests run. In the tests and all trees they are part of the default build,
# in a game's trees (where the tests are on as well) only of that target.
#
# Common options: [TAGS <tag>...] [REQUIRES gpu|display|network|http_server ...] [TIMEOUT <seconds>, 600 by default]
# [SERIAL] (never runs in parallel with other tests) [PLATFORMS <platform>...] (nothing is added for other targets).
# Exit code 77 means skipped. Tests that run programs of the tree are added only when the tree is not cross-compiled.
# DAGOR_TEST_UPDATE_REFERENCES=1 in the environment makes image tests replace their reference images.
include_guard(GLOBAL)

set(_dagor_tests_default OFF)
if(DAGOR_VARIANT MATCHES "^(tests|all)$" OR (DAGOR_VARIANT STREQUAL "game" AND NOT DAGOR_DAS_AOT_COMPILER))
  set(_dagor_tests_default ON)
endif()
option(DAGOR_BUILD_TESTS "Register the tests (the tests and all trees, a game's); off, dagor_add_*_test() do nothing"
  ${_dagor_tests_default})
unset(_dagor_tests_default)

set(DAGOR_TEST_REQUIREMENTS gpu display network http_server)
set(DAGOR_TEST_DEFAULT_TIMEOUT 600)
set(_DAGOR_TEST_ONE_VALUE TIMEOUT CASE_TIMEOUT DATA_DIR WORKING_DIRECTORY PROJECT)
set(_DAGOR_TEST_MULTI_VALUE TAGS REQUIRES PLATFORMS ARGS)
set(_DAGOR_TEST_OPTIONS SERIAL ISOLATED)

# splits the arguments of a test that is also a program: <test-out> gets the test keywords (TAGS, TIMEOUT, ...) with
# their values, <exe-out> the dagor_add_executable ones
function(_dagor_split_test_args test_out exe_out)
  set(test_keywords ${_DAGOR_TEST_OPTIONS} ${_DAGOR_TEST_ONE_VALUE} ${_DAGOR_TEST_MULTI_VALUE})
  set(exe_keywords ${_DAGOR_TARGET_OPTIONS} ${_DAGOR_TARGET_ONE_VALUE} ${_DAGOR_TARGET_MULTI_VALUE})
  set(test_args)
  set(exe_args)
  set(to_test ON)
  foreach(arg IN LISTS ARGN)
    if(arg IN_LIST test_keywords)
      set(to_test ON)
    elseif(arg IN_LIST exe_keywords)
      set(to_test OFF)
    endif()
    if(to_test)
      list(APPEND test_args "${arg}")
    else()
      list(APPEND exe_args "${arg}")
    endif()
  endforeach()
  set(${test_out} "${test_args}" PARENT_SCOPE)
  set(${exe_out} "${exe_args}" PARENT_SCOPE)
endfunction()

# the common options of a test function's parsed arguments (prefix arg_), for _dagor_test_properties: a function with
# keywords of its own does not pass its ARGN on, in which a value would go to the keyword before it
function(_dagor_test_common_args out)
  set(args)
  foreach(option IN LISTS _DAGOR_TEST_OPTIONS)
    if(arg_${option})
      list(APPEND args ${option})
    endif()
  endforeach()
  foreach(keyword IN LISTS _DAGOR_TEST_ONE_VALUE _DAGOR_TEST_MULTI_VALUE)
    if(DEFINED arg_${keyword})
      list(APPEND args ${keyword} ${arg_${keyword}})
    endif()
  endforeach()
  set(${out} "${args}" PARENT_SCOPE)
endfunction()

# a program the tests run: built by the target tests (see the top)
function(_dagor_test_program target)
  set_property(GLOBAL APPEND PROPERTY DAGOR_TEST_PROGRAMS ${target})
endfunction()

# the target tests, at dagor_finalize: the programs exist then (the das interpreter is in a lazily added dir)
function(_dagor_tests_target)
  if(NOT DAGOR_BUILD_TESTS)
    return()
  endif()
  add_custom_target(tests)
  get_property(programs GLOBAL PROPERTY DAGOR_TEST_PROGRAMS)
  if(programs)
    list(REMOVE_DUPLICATES programs)
    add_dependencies(tests ${programs})
    if(NOT DAGOR_VARIANT MATCHES "^(tests|all)$")
      set_target_properties(${programs} PROPERTIES EXCLUDE_FROM_ALL ON)
    endif()
  endif()
endfunction()

# the CTest properties of a test: timeout, serialization, skip code in <out>, its labels in <out>_LABELS
function(_dagor_test_properties out layer)
  cmake_parse_arguments(PARSE_ARGV 2 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}")
  foreach(r IN LISTS arg_REQUIRES)
    dagor_check_choice(REQUIRES "${r}" ${DAGOR_TEST_REQUIREMENTS})
  endforeach()
  set(labels "${layer}" ${arg_TAGS})
  set(requires ${arg_REQUIRES})
  list(TRANSFORM requires PREPEND "requires-")
  list(APPEND labels ${requires})
  if(NOT arg_TIMEOUT)
    set(arg_TIMEOUT ${DAGOR_TEST_DEFAULT_TIMEOUT})
  endif()
  set(props TIMEOUT ${arg_TIMEOUT} SKIP_RETURN_CODE 77)
  if(arg_SERIAL OR "gpu" IN_LIST arg_REQUIRES)
    list(APPEND props RUN_SERIAL TRUE)
  endif()
  set(${out} "${props}" PARENT_SCOPE)
  set(${out}_LABELS "${labels}" PARENT_SCOPE)
endfunction()

# whether a test for <platforms> belongs to this tree (empty: every platform); a game's trees have the tests of the
# project's dirs, not those of the engine dirs its programs use
function(_dagor_test_platform_ok out)
  set(foreign OFF)
  if(DAGOR_VARIANT STREQUAL "game")
    cmake_path(IS_PREFIX CMAKE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE own)
    if(NOT own)
      set(foreign ON)
    endif()
  endif()
  if(NOT DAGOR_BUILD_TESTS OR foreign OR (ARGN AND NOT DAGOR_PLATFORM IN_LIST ARGN))
    set(${out} OFF PARENT_SCOPE)
  else()
    set(${out} ON PARENT_SCOPE)
  endif()
endfunction()

# dagor_add_catch2_test(<name> [DATA_DIR <dir>] [CASE_TIMEOUT <s>] [ARGS ...] <common options>
#   <dagor_add_executable options>): DATA_DIR (default: the calling dir) is where the program finds its test data
#   (--data-dir). TIMEOUT applies to each case, CASE_TIMEOUT makes the program abort a hung case itself.
function(dagor_add_catch2_test name)
  _dagor_split_test_args(test_args exe_args ${ARGN})
  cmake_parse_arguments(arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}" ${test_args})
  _dagor_test_platform_ok(ok ${arg_PLATFORMS})
  if(NOT ok)
    return()
  endif()
  set(data_dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_DATA_DIR)
    _dagor_abs_paths(data_dir "${arg_DATA_DIR}")
  endif()

  # the remaining arguments are the program's (dagor_add_executable); Catch2 reports failures with exceptions
  if(arg_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "dagor_add_catch2_test(${name}): unexpected arguments: ${arg_UNPARSED_ARGUMENTS}")
  endif()
  if(NOT "EXCEPTIONS" IN_LIST exe_args)
    list(APPEND exe_args EXCEPTIONS ON)
  endif()
  dagor_add_executable(${name} CONSOLE OUTPUT_DIR "${CMAKE_BINARY_DIR}/tests" ${exe_args})
  _dagor_test_program(${name})
  _dagor_link(${name} PRIVATE 3rdPartyLibs/catch2 engine/unitTest)
  target_compile_definitions(${name} PRIVATE "UNITTEST_DEFAULT_DATA_DIR=\"${data_dir}\"")

  _dagor_catch2_register(${name} ${name} "${data_dir}" ${test_args})
endfunction()

# dagor_add_catch2_run(<target> <name> [DATA_DIR <dir>] [ARGS ...] <common options>): another run of the cases of a
# dagor_add_catch2_test program, with other arguments and requirements (e.g. on the stub 3d driver); its tests are
# named <name>:<case>
function(dagor_add_catch2_run target name)
  cmake_parse_arguments(PARSE_ARGV 2 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}")
  _dagor_test_platform_ok(ok ${arg_PLATFORMS})
  if(NOT ok OR NOT TARGET ${target})
    return()
  endif()
  set(data_dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_DATA_DIR)
    _dagor_abs_paths(data_dir "${arg_DATA_DIR}")
  endif()
  _dagor_catch2_register(${target} ${name} "${data_dir}" ${ARGN})
endfunction()

# CTest tests <name>:<case> for the cases of the Catch2 program <target>
function(_dagor_catch2_register target name data_dir)
  cmake_parse_arguments(PARSE_ARGV 3 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}")
  if(DAGOR_CROSS_COMPILING)
    return()
  endif()
  _dagor_test_properties(props cpp ${ARGN})
  set(extra --data-dir "${data_dir}" --artifact-dir "${CMAKE_BINARY_DIR}/test-artifacts/${name}" ${arg_ARGS})
  if(arg_CASE_TIMEOUT)
    list(APPEND extra --case-timeout ${arg_CASE_TIMEOUT})
  endif()
  if("http_server" IN_LIST arg_REQUIRES)
    # Catch2's discovery runs the program and its cases through this launcher (its 'emulator')
    set_property(TARGET ${target} PROPERTY CROSSCOMPILING_EMULATOR
      "${Python3_EXECUTABLE};${DAGOR_CMAKE_DIR}/scripts/run_with_http_server.py;${CMAKE_BINARY_DIR}/test-artifacts/${name}/http")
  endif()
  catch_discover_tests(${target}
    TEST_PREFIX "${name}:"
    EXTRA_ARGS ${extra}
    WORKING_DIRECTORY "${data_dir}"
    DISCOVERY_MODE PRE_TEST
    SKIP_IS_FAILURE # the unit test main reports skips as 77, not as Catch2's 4
    TEST_LIST "${name}_TESTS"
    PROPERTIES ${props})
  # the labels reach the discovered cases through an include file CTest reads after Catch2's: the PROPERTIES of
  # catch_discover_tests cannot carry a list value
  set(labels_file "${CMAKE_CURRENT_BINARY_DIR}/${name}_labels.cmake")
  file(CONFIGURE OUTPUT "${labels_file}" @ONLY CONTENT [[
if(@name@_TESTS)
  set_tests_properties(${@name@_TESTS} PROPERTIES LABELS "@props_LABELS@")
endif()
]])
  set_property(DIRECTORY APPEND PROPERTY TEST_INCLUDE_FILES "${labels_file}")
endfunction()

# dagor_add_exec_test(<name> COMMAND <command>... [WORKING_DIRECTORY <dir>] <common options>): the command's
# arguments may use generator expressions ($<TARGET_FILE:...>); DAGOR_TEST_OUT in its environment is a dir for its
# extra results
function(dagor_add_exec_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}"
                        "${_DAGOR_TEST_MULTI_VALUE};COMMAND")
  _dagor_test_platform_ok(ok ${arg_PLATFORMS})
  if(NOT ok)
    return()
  endif()
  if(NOT arg_COMMAND)
    message(FATAL_ERROR "dagor_add_exec_test(${name}) needs a COMMAND")
  endif()
  set(dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_WORKING_DIRECTORY)
    _dagor_abs_paths(dir "${arg_WORKING_DIRECTORY}")
  endif()
  set(command ${arg_COMMAND} ${arg_ARGS})
  if("http_server" IN_LIST arg_REQUIRES)
    list(PREPEND command "${Python3_EXECUTABLE}" "${DAGOR_CMAKE_DIR}/scripts/run_with_http_server.py"
         "${CMAKE_BINARY_DIR}/test-artifacts/${name}/http")
  endif()
  add_test(NAME ${name} COMMAND ${command} WORKING_DIRECTORY "${dir}")
  _dagor_test_common_args(common)
  _dagor_test_properties(props exec ${common})
  set_tests_properties(${name} PROPERTIES ${props} LABELS "${props_LABELS}"
    ENVIRONMENT "DAGOR_TEST_OUT=${CMAKE_BINARY_DIR}/test-artifacts/${name}")
endfunction()

# dagor_add_das_test(<name> PATHS <dir or file>... [PROJECT <.das_project>] [ISOLATED] <common options>): runs dastest
# on the tests with the engine's das interpreter (prog/1stPartyLibs/daScript/utils/daScript)
function(dagor_add_das_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}"
                        "${_DAGOR_TEST_MULTI_VALUE};PATHS")
  _dagor_test_platform_ok(ok ${arg_PLATFORMS})
  if(NOT ok OR DAGOR_CROSS_COMPILING)
    return()
  endif()
  dagor_use(1stPartyLibs/daScript/utils/daScript)
  _dagor_test_program(das)
  set(root "${DAGOR_PROG_DIR}/1stPartyLibs/daScript")
  if(NOT arg_TIMEOUT)
    set(arg_TIMEOUT ${DAGOR_TEST_DEFAULT_TIMEOUT})
  endif()
  set(command $<TARGET_FILE:das> -dasroot "${root}" "${root}/dastest/dastest.das" --)
  _dagor_abs_paths(paths ${arg_PATHS})
  foreach(path IN LISTS paths)
    list(APPEND command --test "${path}")
  endforeach()
  if(arg_PROJECT)
    _dagor_abs_paths(project "${arg_PROJECT}")
    list(APPEND command --test-project "${project}")
  endif()
  if(arg_ISOLATED)
    list(APPEND command --isolated-mode)
  endif()
  # dastest stops itself at --timeout; CTest's limit is a backstop for hangs outside of the tests
  list(APPEND command --timeout ${arg_TIMEOUT} --failures-only ${arg_ARGS})
  add_test(NAME ${name} COMMAND ${command} WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
  math(EXPR backstop "${arg_TIMEOUT} + 60")
  _dagor_test_common_args(common)
  _dagor_test_properties(props das ${common})
  set_tests_properties(${name} PROPERTIES ${props} LABELS "${props_LABELS}" TIMEOUT ${backstop})
endfunction()

# dagor_add_game_test(<name> LAYER ecs|scenario PATHS <dir or file>... [SCENE <scene .blk>] [CASE_TIMEOUT <s>]
#   [ARGS ...] <common options>): the [ecs_test] functions of the .das files run by the game of the tree
#   (dagor_add_dng_game, before it) in its test mode (prog/daNetGame/main/testMode.h), from the game dir (the parent of
#   its output dir), which SCENE is relative to. ecs tests belong in the dedicated server's tree; scenario tests render,
#   compare their screenshots with references/ next to them and need a GPU and a display: the client's tree. Their
#   results and screenshots go to test-artifacts/<name> in the build dir.
function(dagor_add_game_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE};LAYER;SCENE"
                        "${_DAGOR_TEST_MULTI_VALUE};PATHS")
  _dagor_test_platform_ok(ok ${arg_PLATFORMS})
  if(NOT ok OR DAGOR_CROSS_COMPILING)
    return()
  endif()
  dagor_check_choice(LAYER "${arg_LAYER}" ecs scenario)
  get_property(game GLOBAL PROPERTY DAGOR_GAME_TARGET)
  if(NOT game)
    message(FATAL_ERROR "dagor_add_game_test(${name}): the tree has no game (dagor_add_dng_game() comes first)")
  endif()
  if(NOT arg_PATHS)
    message(FATAL_ERROR "dagor_add_game_test(${name}) needs PATHS")
  endif()
  set(out "${CMAKE_BINARY_DIR}/test-artifacts/${name}")
  set(args -stdout -quiet -nolisten -nostatsd -nonetenc -nopeerauth
    -config:debug/useAddonVromSrc:b=yes   # tests and test libs are read from the sources, no repacking needed
    -config:debug/daScriptHotReload:b=no  # running tests hold pointers into loaded scripts
    "-test_out:${out}")
  _dagor_abs_paths(paths ${arg_PATHS})
  foreach(path IN LISTS paths)
    list(APPEND args "-das_test:${path}")
  endforeach()
  if(arg_CASE_TIMEOUT)
    list(APPEND args "-test_timeout:${arg_CASE_TIMEOUT}")
  endif()
  if(arg_SCENE)
    list(APPEND args "-scene:${arg_SCENE}")
  endif()
  if(arg_LAYER STREQUAL "scenario")
    list(APPEND arg_REQUIRES gpu display)
    list(REMOVE_DUPLICATES arg_REQUIRES)
    list(APPEND args -config:video/mode:t=windowed -config:video/resolution:t=1280x720
      -config:screenshots/format:t=png "-config:screenshots/dir:t=${out}/screenshots"
      # no physical keyboard, mouse or joystick (values <= 0 are added to All=7): what a person does on the machine
      # must not leak into the test; scripted input (send_action, set_axis) works without them
      -config:input/hidDriversInit:i=-7
      # temporal antialiasing jitters by the global frame index, which depends on how many frames loading took:
      # screenshots would differ run to run at every edge
      -config:video/antialiasing_mode:t=off)
  endif()
  add_test(NAME ${name}
    COMMAND "${Python3_EXECUTABLE}" "${DAGOR_CMAKE_DIR}/scripts/run_game_test.py" "${out}" $<TARGET_FILE:${game}>
            ${args} ${arg_ARGS}
    WORKING_DIRECTORY "$<PATH:GET_PARENT_PATH,$<TARGET_FILE_DIR:${game}>>")
  _dagor_test_common_args(common)
  _dagor_test_properties(props ${arg_LAYER} ${common})
  set_tests_properties(${name} PROPERTIES ${props} LABELS "${props_LABELS}")
endfunction()

# dagor_use_tests(): adds every engine directory that declares tests (in the tests and all trees)
function(dagor_use_tests)
  file(GLOB_RECURSE lists RELATIVE "${DAGOR_PROG_DIR}" "${DAGOR_PROG_DIR}/*/CMakeLists.txt")
  foreach(list IN LISTS lists)
    if(list MATCHES "(^|/)(3rdPartyLibs|_output|_jBuild)/")
      continue()
    endif()
    file(STRINGS "${DAGOR_PROG_DIR}/${list}" registers REGEX "^[ \t]*dagor_add_[a-z0-9]+_test\\(" LIMIT_COUNT 1)
    if(registers)
      cmake_path(GET list PARENT_PATH ref)
      dagor_use("${ref}")
    endif()
  endforeach()
endfunction()

enable_testing()
include("${DAGOR_PROG_DIR}/3rdPartyLibs/catch2/extras/Catch.cmake")
