
dagor_add_target(NAME dag_convinst EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE dagConvInst_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.lib3d
    engine.math engine.perfMon.daProfilerStub tools.libTools.util tools.libTools.dagFileRW
)
