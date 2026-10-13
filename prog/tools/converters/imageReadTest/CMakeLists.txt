set(deps
  engine.osApiWrappers
  engine.kernel
  engine.memory
  engine.ioSys
  engine.startup
  engine.baseUtil
  engine.math
  engine.image
  engine.drv.drv3d_null
  engine.perfMon.daProfilerStub
  3rdPartyLibs.image.psdRead
  3rdPartyLibs.image.libpng-1.4.22
  3rdPartyLibs.image.avif
  3rdPartyLibs.image.tiff-4.4.0
  3rdPartyLibs.image.jpeg-6b
)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME imageReadTest EXECUTABLE LAX
  FILES_CMAKE imageReadTest_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
  CDK
)
