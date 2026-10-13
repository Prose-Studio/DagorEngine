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
