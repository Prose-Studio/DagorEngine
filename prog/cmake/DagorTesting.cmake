# Tests, run by CTest (ctest --preset <preset>). Each test gets the CTest labels of its layer (cpp, das, exec, ecs,
# scenario), its TAGS and its REQUIRES as requires-<what>: the ci test presets exclude requires-gpu|requires-display.
#
#   dagor_add_catch2_test(<name> [DATA_DIR <dir>] [CASE_TIMEOUT <s>] [ARGS ...] [LAX] <common> [<source>...])
#       a Catch2 program (main from <unittest/mainCatch2.inc.cpp>); each test case is a CTest test <name>:<case>.
#       DATA_DIR (default: the calling dir) is where it finds its test data (--data-dir); CASE_TIMEOUT makes it abort
#       a hung case itself. The program is target <name>: link its libraries with target_link_libraries.
#   dagor_add_catch2_run(<target> <name> [DATA_DIR <dir>] [ARGS ...] <common>)
#       another run of a dagor_add_catch2_test program's cases with other arguments and requirements (<name>:<case>)
#   dagor_add_das_test(<name> PATHS <dir or file>... [PROJECT <.das_project>] [ISOLATED] [WORKING_DIRECTORY <dir>]
#                      <common>)
#       daScript [test] functions run by dastest on the engine's das interpreter
#   dagor_add_exec_test(<name> COMMAND <command>... [WORKING_DIRECTORY <dir>] <common>)
#       any command (generator expressions allowed); its exit code is the result
#   dagor_add_game_test(<name> LAYER ecs|scenario PATHS <dir or file>... [SCENE <scene .blk>] [CASE_TIMEOUT <s>]
#                       [ARGS ...] <common>)
#       [ecs_test] functions run by the tree's game in its test mode (prog/daNetGame/main/testMode.h), from the game
#       dir; ecs tests belong in the dedicated server's tree, scenario tests (which render and compare screenshots with
#       references/ next to them) in the client's. Their results go to <build>/test-artifacts/<name>.
#
# <common>: [TAGS <tag>...] [REQUIRES gpu|display|network|http_server ...] [TIMEOUT <seconds>, 600 by default]
# [SERIAL] (never in parallel with other tests) [PLATFORMS <platform>...] (DAGOR_PLATFORM names; nothing is registered
# for other targets). Exit code 77 means skipped. DAGOR_TEST_UPDATE_REFERENCES=1 in the environment makes image tests
# replace their reference images.
#
# Tests are registered with DAGOR_BUILD_TESTS; the engine's own only in the engine's trees (not in a project's, which
# have the project's tests), and none that run programs of a cross-compiled tree without an emulator. The target tests
# builds the programs they run; in the tests variant they are part of the default build.
include_guard(GLOBAL)

set(_dagor_tests_default OFF)
if(DAGOR_VARIANT STREQUAL "tests" OR (DAGOR_VARIANT STREQUAL "game" AND NOT DAGOR_DAS_AOT_COMPILER))
  set(_dagor_tests_default ON)
endif()
option(DAGOR_BUILD_TESTS "Register the tests" ${_dagor_tests_default})
unset(_dagor_tests_default)

set(DAGOR_TEST_REQUIREMENTS gpu display network http_server)
set(_DAGOR_TEST_OPTIONS SERIAL ISOLATED)
set(_DAGOR_TEST_ONE_VALUE TIMEOUT CASE_TIMEOUT DATA_DIR WORKING_DIRECTORY PROJECT)
set(_DAGOR_TEST_MULTI_VALUE TAGS REQUIRES PLATFORMS ARGS)

enable_testing()
include("${DAGOR_PROG_DIR}/3rdPartyLibs/catch2/extras/Catch.cmake")
add_custom_target(tests)
set_property(TARGET tests PROPERTY FOLDER "dagor")

# _dagor_test_enabled(<out> <platforms>...): whether the calling dir registers its tests (see the top); <out>_RUNS whether
# the tree can run its programs
function(_dagor_test_enabled out)
  cmake_path(IS_PREFIX DAGOR_PROG_DIR "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE in_engine)
  set(ok ${DAGOR_BUILD_TESTS})
  if(in_engine AND NOT CMAKE_SOURCE_DIR STREQUAL DAGOR_PROG_DIR)
    set(ok OFF)
  endif()
  if(ARGN AND NOT DAGOR_PLATFORM IN_LIST ARGN)
    set(ok OFF)
  endif()
  set(runs ON)
  if(CMAKE_CROSSCOMPILING AND NOT CMAKE_CROSSCOMPILING_EMULATOR)
    set(runs OFF)
  endif()
  set(${out} ${ok} PARENT_SCOPE)
  set(${out}_RUNS ${runs} PARENT_SCOPE)
endfunction()

# a program the tests run: built by the target tests, and by default in the tests variant (once the tree is complete:
# the das interpreter's dir comes after the dirs of the tests it runs)
function(_dagor_test_program target)
  add_dependencies(tests ${target})
  if(DAGOR_VARIANT STREQUAL "tests")
    cmake_language(DEFER DIRECTORY "${CMAKE_SOURCE_DIR}" CALL dagor_build_by_default ${target})
  endif()
endfunction()

# the CTest properties of a test (the calling function's arg_*): timeout, serialization, skip code in <out>, its labels
# in <out>_LABELS
function(_dagor_test_properties out layer)
  foreach(r IN LISTS arg_REQUIRES)
    dagor_check_choice(REQUIRES "${r}" ${DAGOR_TEST_REQUIREMENTS})
  endforeach()
  set(requires ${arg_REQUIRES})
  list(TRANSFORM requires PREPEND "requires-")
  set(timeout ${arg_TIMEOUT})
  if(NOT timeout)
    set(timeout 600)
  endif()
  set(props TIMEOUT ${timeout} SKIP_RETURN_CODE 77)
  if(arg_SERIAL OR "gpu" IN_LIST arg_REQUIRES)
    list(APPEND props RUN_SERIAL TRUE)
  endif()
  set(${out} "${props}" PARENT_SCOPE)
  set(${out}_LABELS "${layer};${arg_TAGS};${requires}" PARENT_SCOPE)
endfunction()

# the dir a test works in by default, under <build>/test-artifacts
function(_dagor_test_artifacts name out)
  set(dir "${CMAKE_BINARY_DIR}/test-artifacts/${name}")
  file(MAKE_DIRECTORY "${dir}")
  set(${out} "${dir}" PARENT_SCOPE)
endfunction()

# a command run with the HTTP test server (REQUIRES http_server)
function(_dagor_http_launcher name out)
  set(${out} "${Python3_EXECUTABLE}" "${DAGOR_CMAKE_DIR}/scripts/run_with_http_server.py"
    "${CMAKE_BINARY_DIR}/test-artifacts/${name}/http" PARENT_SCOPE)
endfunction()

# the program is made whether or not its tests are registered, so the commands that follow can set it up
function(dagor_add_catch2_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS};LAX" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}")
  set(lax)
  if(arg_LAX)
    set(lax LAX)
  endif()
  dagor_add_executable(${name} ${lax} OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/tests" ${arg_UNPARSED_ARGUMENTS})
  set_property(TARGET ${name} PROPERTY DAGOR_EXCEPTIONS ON) # Catch2 reports failures with exceptions
  target_link_libraries(${name} PRIVATE 3rdPartyLibs.catch2 engine.unitTest)
  set(data_dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_DATA_DIR)
    cmake_path(ABSOLUTE_PATH arg_DATA_DIR NORMALIZE OUTPUT_VARIABLE data_dir)
  endif()
  target_compile_definitions(${name} PRIVATE "UNITTEST_DEFAULT_DATA_DIR=\"${data_dir}\"")
  _dagor_test_enabled(ok ${arg_PLATFORMS})
  if(NOT ok)
    return()
  endif()
  _dagor_test_program(${name})
  if(ok_RUNS)
    _dagor_catch2_register(${name} ${name} "${data_dir}")
  endif()
endfunction()

function(dagor_add_catch2_run target name)
  cmake_parse_arguments(PARSE_ARGV 2 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}" "${_DAGOR_TEST_MULTI_VALUE}")
  _dagor_test_enabled(ok ${arg_PLATFORMS})
  if(NOT ok OR NOT ok_RUNS)
    return()
  endif()
  set(data_dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_DATA_DIR)
    cmake_path(ABSOLUTE_PATH arg_DATA_DIR NORMALIZE OUTPUT_VARIABLE data_dir)
  endif()
  _dagor_catch2_register(${target} ${name} "${data_dir}")
endfunction()

# CTest tests <name>:<case> for the cases of the Catch2 program <target> (the calling function's arg_*)
function(_dagor_catch2_register target name data_dir)
  _dagor_test_properties(props cpp)
  set(extra --data-dir "${data_dir}" --artifact-dir "${CMAKE_BINARY_DIR}/test-artifacts/${name}" ${arg_ARGS})
  if(arg_CASE_TIMEOUT)
    list(APPEND extra --case-timeout ${arg_CASE_TIMEOUT})
  endif()
  if("http_server" IN_LIST arg_REQUIRES)
    # Catch2's discovery runs the program and its cases through this launcher (its 'emulator')
    _dagor_http_launcher(${name} launcher)
    set_property(TARGET ${target} PROPERTY CROSSCOMPILING_EMULATOR "${launcher}")
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

# adds test <name> running <command> in <dir> with the properties of <layer> (the calling function's arg_*)
function(_dagor_add_test name layer dir)
  add_test(NAME ${name} COMMAND ${ARGN} WORKING_DIRECTORY "${dir}")
  _dagor_test_properties(props ${layer})
  set_tests_properties(${name} PROPERTIES ${props} LABELS "${props_LABELS}")
endfunction()

function(dagor_add_exec_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}"
                        "${_DAGOR_TEST_MULTI_VALUE};COMMAND")
  _dagor_test_enabled(ok ${arg_PLATFORMS})
  if(NOT ok)
    return()
  endif()
  if(NOT arg_COMMAND)
    message(FATAL_ERROR "dagor_add_exec_test(${name}) needs a COMMAND")
  endif()
  set(dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_WORKING_DIRECTORY)
    cmake_path(ABSOLUTE_PATH arg_WORKING_DIRECTORY NORMALIZE OUTPUT_VARIABLE dir)
  endif()
  set(launcher)
  if("http_server" IN_LIST arg_REQUIRES)
    _dagor_http_launcher(${name} launcher)
  endif()
  _dagor_add_test(${name} exec "${dir}" ${launcher} ${arg_COMMAND} ${arg_ARGS})
  set_property(TEST ${name} APPEND PROPERTY ENVIRONMENT "DAGOR_TEST_OUT=${CMAKE_BINARY_DIR}/test-artifacts/${name}")
endfunction()

function(dagor_add_das_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE}"
                        "${_DAGOR_TEST_MULTI_VALUE};PATHS")
  _dagor_test_enabled(ok ${arg_PLATFORMS})
  if(NOT ok OR NOT ok_RUNS)
    return()
  endif()
  _dagor_test_program(das)
  set(root "${DAGOR_PROG_DIR}/1stPartyLibs/daScript")
  if(NOT arg_TIMEOUT)
    set(arg_TIMEOUT 600)
  endif()
  set(command $<TARGET_FILE:das> -dasroot "${root}" "${root}/dastest/dastest.das" --)
  foreach(path IN LISTS arg_PATHS)
    cmake_path(ABSOLUTE_PATH path NORMALIZE)
    list(APPEND command --test "${path}")
  endforeach()
  if(arg_PROJECT)
    cmake_path(ABSOLUTE_PATH arg_PROJECT NORMALIZE OUTPUT_VARIABLE project)
    list(APPEND command --test-project "${project}")
  endif()
  if(arg_ISOLATED)
    list(APPEND command --isolated-mode)
  endif()
  # dastest stops itself at --timeout; CTest's limit is a backstop for hangs outside of the tests
  list(APPEND command --timeout ${arg_TIMEOUT} --failures-only ${arg_ARGS})
  # in a dir of its own unless the tests need theirs: daScript writes its module cache (.jitted_scripts) there
  if(arg_WORKING_DIRECTORY)
    cmake_path(ABSOLUTE_PATH arg_WORKING_DIRECTORY NORMALIZE OUTPUT_VARIABLE dir)
  else()
    _dagor_test_artifacts(${name} dir)
  endif()
  _dagor_add_test(${name} das "${dir}" ${command})
  math(EXPR backstop "${arg_TIMEOUT} + 60")
  set_property(TEST ${name} PROPERTY TIMEOUT ${backstop})
endfunction()

function(dagor_add_game_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "${_DAGOR_TEST_OPTIONS}" "${_DAGOR_TEST_ONE_VALUE};LAYER;SCENE"
                        "${_DAGOR_TEST_MULTI_VALUE};PATHS")
  _dagor_test_enabled(ok ${arg_PLATFORMS})
  if(NOT ok OR NOT ok_RUNS)
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
  _dagor_test_artifacts(${name} out)
  set(args -stdout -quiet -nolisten -nostatsd -nonetenc -nopeerauth
    -config:debug/useAddonVromSrc:b=yes   # tests and test libs are read from the sources, no repacking needed
    -config:debug/daScriptHotReload:b=no  # running tests hold pointers into loaded scripts
    "-test_out:${out}")
  foreach(path IN LISTS arg_PATHS)
    cmake_path(ABSOLUTE_PATH path NORMALIZE)
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
  _dagor_add_test(${name} ${arg_LAYER} "$<PATH:GET_PARENT_PATH,$<TARGET_FILE_DIR:${game}>>"
    "${Python3_EXECUTABLE}" "${DAGOR_CMAKE_DIR}/scripts/run_game_test.py" "${out}" $<TARGET_FILE:${game}> ${args} ${arg_ARGS})
endfunction()
