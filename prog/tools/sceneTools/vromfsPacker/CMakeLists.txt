# vromfsPacker: the virtual ROM file system (vromfs) pack builder (gameLibs/vromfsPacker)
set(deps engine.kernel engine.memory engine.perfMon.daProfilerStub engine.startup engine.math gameLibs.vromfsPacker)
if(WIN32)
  list(APPEND libs System::advapi32)
endif()
if(LINUX)
  set(libs System::dl)
endif()
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME vromfsPacker EXECUTABLE LAX
  FILES_CMAKE vromfsPacker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES
    PUBLIC ${libs}
    PRIVATE ${deps}
  PROPERTIES DAGOR_EXCEPTIONS ON
  CDK
)

# the test (tests/, writing into its DAGOR_TEST_OUT): a directory packed by a build BLK as the games' are, twice the
# same, listed and unpacked to the files the BLK selects and processes for each target (its BLKs read back by binBlk),
# long paths packed, a path past the engine's limit failing the pack
if(DAGOR_CDK_TESTS)
  dagor_add_exec_test(vromfsPacker.pack COMMAND ${Python3_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/tests/vromfs_pack.py
    $<TARGET_FILE:vromfsPacker> $<TARGET_FILE:binBlk> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk
    TIMEOUT 60)
endif()
