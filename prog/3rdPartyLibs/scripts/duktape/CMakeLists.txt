# Duktape 2.2.1, the embeddable ECMAScript engine, built as its command line interpreter (duktape)
if(CMAKE_SYSTEM_NAME MATCHES "^(Darwin|Linux)$")
  list(APPEND options -fno-fast-math -Wno-format-overflow)
endif()

dagor_add_target(NAME duktape EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE duktape_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    examples/cmdline src extras/print-alert extras/console extras/logging extras/module-duktape
  COMPILE_DEFINITIONS PRIVATE
    __B_NO_MEM_BASE_INCLUDE DUK_CMDLINE_PRINTALERT_SUPPORT DUK_CMDLINE_CONSOLE_SUPPORT DUK_CMDLINE_LOGGING_SUPPORT
    DUK_CMDLINE_MODULE_SUPPORT DUK_CMDLINE_FILEIO
  COMPILE_OPTIONS PRIVATE ${options}
  CDK
)

# the tests (tests/): selftest.js checks the language, Duktape's builtins and the command line's extras, run from its
# source and compiled to bytecode (in their DAGOR_TEST_OUT); a script that throws makes the interpreter exit with 1
if(DAGOR_CDK_TESTS)
  foreach(mode source bytecode)
    dagor_add_exec_test(duktape.selftest-${mode} COMMAND ${CMAKE_COMMAND} -DDUKTAPE=$<TARGET_FILE:duktape>
      -DMODE=${mode} -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/selftest.cmake WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
      TAGS cdk TIMEOUT 60)
  endforeach()
  dagor_add_exec_test(duktape.uncaught-error COMMAND ${CMAKE_COMMAND} -DCODE=1
    -P ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake $<TARGET_FILE:duktape> ${CMAKE_CURRENT_SOURCE_DIR}/tests/fails.js
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
endif()
