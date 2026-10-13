# A benchmark of daECS (daECS_benchmark, next to its sources as jam built it; no 3d driver)
dagor_add_target(NAME daECS_benchmark EXECUTABLE
  OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  FILES_CMAKE sample_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.perfMon engine.math engine.baseUtil engine.ioSys
    engine.startup engine.daECS.core engine.daECS.io.datablock
  PROPERTIES DAGOR_NO_GPU ON
)
