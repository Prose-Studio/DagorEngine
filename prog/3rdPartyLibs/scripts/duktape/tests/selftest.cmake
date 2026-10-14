# cmake -DDUKTAPE=<duktape> -DMODE=<source|bytecode> -P selftest.cmake
# Runs selftest.js in the test's dir (DAGOR_TEST_OUT, which CTest sets), from its source or compiled to Duktape bytecode
# first (duktape -c), and fails unless it reports its checks passed (the interpreter skips the files not named *.js, it
# leaves them to the script: an exit code of 0 alone could mean the script did not run).
set(OUT "$ENV{DAGOR_TEST_OUT}")
if(NOT DUKTAPE OR NOT MODE MATCHES "^(source|bytecode)$")
  message(FATAL_ERROR "usage: cmake -DDUKTAPE=<duktape> -DMODE=<source|bytecode> -P selftest.cmake")
endif()
if(NOT OUT)
  message(FATAL_ERROR "DAGOR_TEST_OUT is not set (the tests run through CTest)")
endif()
file(REMOVE_RECURSE "${OUT}")
file(MAKE_DIRECTORY "${OUT}")
set(script "${CMAKE_CURRENT_LIST_DIR}/selftest.js")
if(MODE STREQUAL "bytecode")
  execute_process(COMMAND "${DUKTAPE}" -c selftest.bytecode.js "${script}"
    WORKING_DIRECTORY "${OUT}" RESULT_VARIABLE result OUTPUT_VARIABLE out ERROR_VARIABLE out)
  if(NOT result STREQUAL "0" OR NOT EXISTS "${OUT}/selftest.bytecode.js")
    message(FATAL_ERROR "duktape -c exited with ${result} and wrote no bytecode:\n${out}")
  endif()
  file(READ "${OUT}/selftest.bytecode.js" head LIMIT 1 HEX)
  if(NOT head STREQUAL "bf")
    message(FATAL_ERROR "${OUT}/selftest.bytecode.js is not Duktape bytecode: it starts with ${head}, not bf")
  endif()
  set(script selftest.bytecode.js)
endif()
execute_process(COMMAND "${DUKTAPE}" "${script}"
  WORKING_DIRECTORY "${OUT}" RESULT_VARIABLE result OUTPUT_VARIABLE out ERROR_VARIABLE out)
if(NOT result STREQUAL "0" OR NOT out MATCHES "duktape selftest: [0-9]+ checks passed")
  message(FATAL_ERROR "selftest.js (${MODE}) exited with ${result}:\n${out}")
endif()
message(STATUS "${out}")
