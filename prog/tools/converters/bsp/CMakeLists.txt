dagor_add_target(NAME bsp2dag EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/converters
  FILES_CMAKE bsp_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/converters/ ${DAGOR_PROG_DIR}/tools/converters/bsp
    ${DAGOR_PROG_DIR}/tools/converters/bsp/tier1
  COMPILE_DEFINITIONS PRIVATE __B_MAIN
  BUILD_DEPENDENCIES PRIVATE
    tools.libTools.dagFileRW engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup
    engine.baseUtil engine.math engine.image engine.perfMon.daProfilerStub
)
