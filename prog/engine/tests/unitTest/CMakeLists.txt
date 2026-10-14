# Unit tests of the unit test harness itself (image compare, test environment, failures)
dagor_add_catch2_test(NAME unitTest-tests LAX
  TAGS engine
  FILES_CMAKE unitTest_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.image
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)

# the harness's own checks: its hidden [harness] cases fail on purpose, each the way the harness must report it (exit 1
# with the failure in events.jsonl, 3 for a case the watchdog stops, 77 skipped, a crash, the image check's artifacts)
foreach(check "unexpected logerr fails the case|1|events.jsonl" "logerr on another thread fails the case|1|"
    "expected logerr count mismatch fails|1|" "dagor assertion fails the case|1|" "hung case hits the watchdog|3|"
    "skipped case|77|" "crash fails the case|crash|"
    "image mismatch writes artifacts|1|harness__image_mismatch_writes_artifacts/gradient.diff.png")
  string(REPLACE "|" ";" check "${check}")
  list(GET check 0 case)
  list(GET check 1 code)
  list(GET check 2 file)
  string(MAKE_C_IDENTIFIER "${case}" dir)
  set(art ${CMAKE_BINARY_DIR}/test-artifacts/unitTest-tests.harness/${dir})
  if(file)
    set(file ${art}/${file})
  endif()
  dagor_add_exec_test("unitTest-tests.harness:${case}" COMMAND ${CMAKE_COMMAND} -DCODE=${code} -DFILES=${file}
    -P ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake $<TARGET_FILE:unitTest-tests> "harness: ${case}" --case-timeout 2
    --artifact-dir ${art} --data-dir ${CMAKE_CURRENT_SOURCE_DIR} TAGS engine)
endforeach()
