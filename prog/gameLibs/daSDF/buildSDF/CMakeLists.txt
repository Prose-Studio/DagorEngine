# buildSDF: builds the signed distance fields of models (tools/util, as jam built it)
dagor_add_target(NAME buildSDF EXECUTABLE LAX
  OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE buildSDF_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.daSDF.buildSDFLib engine.osApiWrappers engine.kernel engine.memory engine.baseUtil engine.ioSys
    engine.perfMon.daProfilerStub engine.daBVH engine.math engine.startup
)
