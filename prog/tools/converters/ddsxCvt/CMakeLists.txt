# ddsxCvt: converts DDS textures to the DDSx of a target platform through the DDSx plugins
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.perfMon.daProfilerStub tools.libTools.dtx tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME ddsxCvt EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE ddsxCvt_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# its tests (tests/ddsxCvt_tests.py): textures of each format converted by each platform's plugin (which ddsxCvt loads
# from next to it, so the tests name them to have them built) and read back
if(DAGOR_CDK_TESTS)
  foreach(scenario pc mobile packing errors)
    dagor_add_exec_test(ddsxCvt.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/ddsxCvt_tests.py ${scenario} $<TARGET_FILE:ddsxCvt> $<TARGET_FILE:pcDdsxConv>
      $<TARGET_FILE:iosDdsxConv> $<TARGET_FILE:andDdsxConv> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk
      TIMEOUT 60)
  endforeach()
endif()
