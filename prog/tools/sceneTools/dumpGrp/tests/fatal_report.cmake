# cmake -DDUMPGRP=<dumpGrp> -P fatal_report.cmake (in DAGOR_TEST_OUT)
# A console program's fatal error (dumpGrp's on truncated.grp, whose data runs past its end) is reported on its console
# and ends the run: it must not wait in a message box for someone to close it, which holds an unattended run.
set(OUT "$ENV{DAGOR_TEST_OUT}")
if(NOT DUMPGRP)
  message(FATAL_ERROR "usage: cmake -DDUMPGRP=<dumpGrp> -P fatal_report.cmake")
endif()
if(NOT OUT)
  message(FATAL_ERROR "DAGOR_TEST_OUT is not set (the tests run through CTest)")
endif()
file(REMOVE_RECURSE "${OUT}")
file(MAKE_DIRECTORY "${OUT}")
execute_process(COMMAND "${DUMPGRP}" "${CMAKE_CURRENT_LIST_DIR}/truncated.grp" -dump WORKING_DIRECTORY "${OUT}"
  RESULT_VARIABLE result OUTPUT_VARIABLE out ERROR_VARIABLE err TIMEOUT 30)
if(NOT result MATCHES "^[1-9][0-9]*$") # not a clean exit with an error code: a crash, or killed while waiting
  message(FATAL_ERROR "dumpGrp ended with ${result}:\n${out}\n${err}")
endif()
if(NOT err MATCHES "read error")
  message(FATAL_ERROR "dumpGrp exited with ${result} but did not report the fatal error on stderr:\n${err}")
endif()
