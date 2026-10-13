dagor_add_target(NAME gmt2dag EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE gmt2dag_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.baseUtil engine.perfMon.daProfilerStub
    tools.libTools.dagFileRW
)
