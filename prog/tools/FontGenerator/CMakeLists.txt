# fontgen2: builds the engine's bitmap/SDF font atlases from TrueType/OpenType fonts (FreeType, HarfBuzz)
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.image engine.perfMon.daProfilerStub tools.libTools.dtx tools.libTools.util 3rdPartyLibs.freetype.freetype-2.8
  3rdPartyLibs.image.psdRead 3rdPartyLibs.image.libpng-1.4.22 3rdPartyLibs.image.avif 3rdPartyLibs.image.jpeg-6b)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME fontgen2 EXECUTABLE LAX
  FILES_CMAKE FontGenerator_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/freetype/freetype-2.8/include ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# its tests (tests/fontgen2_tests.py): dargbox's fully dynamic fonts built again as committed, a baked atlas read back
# as the engine loads it, broken rules
if(DAGOR_CDK_TESTS)
  foreach(scenario dynamic baked errors)
    dagor_add_exec_test(fontgen2.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/fontgen2_tests.py ${scenario} $<TARGET_FILE:fontgen2>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
endif()
