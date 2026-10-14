# csvUtil2: processes localization CSV files by BLK tasks; inserts word breaks into Japanese and Chinese text
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.coreUtil engine.perfMon.daProfilerStub 3rdPartyLibs.regExp)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME csvUtil2 EXECUTABLE LAX
  FILES_CMAKE csvUtil_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# the tests (tests/csv_util.py, writing into their DAGOR_TEST_OUT): a localization task BLK's CSV and value dump (and
# that CSV read back the same), the task BLK run without task names, the Japanese and Chinese word breaks
if(DAGOR_CDK_TESTS)
  foreach(scenario localization all-tasks word-breaks)
    dagor_add_exec_test(csvUtil2.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/csv_util.py ${scenario} $<TARGET_FILE:csvUtil2>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
endif()
