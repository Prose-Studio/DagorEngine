dagor_add_target(NAME strmBuild EXECUTABLE LAX
  FILES_CMAKE strmBuild_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.math engine.baseUtil engine.ioSys engine.startup
    engine.lib3d engine.shaders engine.drv.drv3d_stub engine.scene engine.perfMon
  CDK
)
