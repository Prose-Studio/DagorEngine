# convertToChromeTrace: converts a daProfiler dump to a Chrome trace (tools/util, as jam built it)
dagor_add_target(NAME convertToChromeTrace EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE convertToChromeTrace_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.perfMon.daProfilerStub
    3rdPartyLibs.eastl
)
