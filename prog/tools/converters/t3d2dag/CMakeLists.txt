dagor_add_target(NAME t3d2dag EXECUTABLE LAX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters/t3d2dag
  FILES_CMAKE t3d2dag_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools
  COMPILE_DEFINITIONS PRIVATE DOUBLE=double
  BUILD_DEPENDENCIES PRIVATE
    tools.libTools.dagFileRW engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup
    engine.baseUtil engine.math engine.image engine.lib3d engine.perfMon.daProfilerStub
)
