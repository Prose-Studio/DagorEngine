dagor_add_target(NAME scnUtil EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE scnUtil_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    engine.perfMon.daProfilerStub
)
