# addSymbols: adds the symbols of the programs to a daProfiler dump (tools/util, as jam built it)
dagor_add_target(NAME addSymbols EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE addSymbols_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys engine.perfMon.daProfilerStub
    3rdPartyLibs.eastl
)
