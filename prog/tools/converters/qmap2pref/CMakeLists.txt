dagor_add_target(NAME qmap2pref EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters
  FILES_CMAKE qmap2pref_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub tools.libTools.util
)
