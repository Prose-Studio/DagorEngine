# ddsConverter: converts images to DDS textures
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.image engine.drv.drv3d_null engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dtx
  3rdPartyLibs.image.psdRead 3rdPartyLibs.image.libpng-1.4.22)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME ddsConverter EXECUTABLE LAX
  FILES_CMAKE ddsConverter_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
# its ASTC formats are encoded by ARM's astcenc, which it runs from its own dir
find_package(Astcenc REQUIRED)
dagor_target_runtime_files(ddsConverter ${Astcenc_PROGRAMS})

# its tests (tests/ddsConverter_tests.py): images converted in each format, their pixels read back and compared
if(DAGOR_CDK_TESTS)
  foreach(scenario argb dxt astc formats errors)
    dagor_add_exec_test(ddsConverter.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/ddsConverter_tests.py ${scenario} $<TARGET_FILE:ddsConverter>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
endif()
