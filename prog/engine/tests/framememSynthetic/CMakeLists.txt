# A synthetic benchmark of the frame memory allocator (a program, not a test)
dagor_add_target(NAME testFramememSynthetic EXECUTABLE
  FILES_CMAKE framememSynthetic_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ..
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.startup engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub engine.perfMon.perfTimerStub
)
