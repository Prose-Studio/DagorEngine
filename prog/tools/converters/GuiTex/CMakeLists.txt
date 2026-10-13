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
