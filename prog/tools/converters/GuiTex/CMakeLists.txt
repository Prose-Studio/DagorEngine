# guiTex: builds GUI texture atlases (DDS/DDSx with coordinate BLKs) from icon folders, and unpacks them
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
  engine.image engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dtx 3rdPartyLibs.image.psdRead
  3rdPartyLibs.image.libpng-1.4.22)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME guiTex EXECUTABLE LAX
  FILES_CMAKE GuiTex_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)

# its tests (tests/guiTex_tests.py): an atlas of icons, as DDS, DDSx (with the PC plugin) and bundle, read back and
# compared with the icons, and unpacked again
if(DAGOR_CDK_TESTS)
  foreach(scenario atlas ddsx unpack)
    dagor_add_exec_test(guiTex.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/guiTex_tests.py ${scenario} $<TARGET_FILE:guiTex> $<TARGET_FILE:pcDdsxConv>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
endif()
