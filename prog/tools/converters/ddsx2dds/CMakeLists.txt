# ddsx2dds: converts DDSx textures back to DDS (PC formats) and dumps their headers
dagor_add_target(NAME ddsx2dds EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE ddsx2dds_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.osApiWrappers.messageBox.stub engine.kernel engine.memory engine.ioSys engine.startup
    engine.baseUtil engine.math engine.perfMon.daProfilerStub
  CDK
)
# -decodeASTC decodes with ARM's astcenc, which it runs from its own dir
find_package(Astcenc REQUIRED)
dagor_target_runtime_files(ddsx2dds ${Astcenc_PROGRAMS})

# its tests (tests/ddsx2dds_tests.py, on the readers of tests/texfiles.py the CDK's other image tests share): DDSx made
# by ddsxCvt (with the PC plugin, the iOS one for ASTC) converted back, dumped, checked and decoded, and broken ones
if(DAGOR_CDK_TESTS)
  foreach(scenario roundtrip dump check bundle astc invalid)
    dagor_add_exec_test(ddsx2dds.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/ddsx2dds_tests.py ${scenario} $<TARGET_FILE:ddsxCvt> $<TARGET_FILE:ddsx2dds>
      $<TARGET_FILE:pcDdsxConv> $<TARGET_FILE:iosDdsxConv> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk
      TIMEOUT 60)
  endforeach()
endif()
