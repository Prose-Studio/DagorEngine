dagor_add_target(NAME sbmp2sbp1 EXECUTABLE LAX NO_CONFIG_POSTFIX OUTPUT_DIRECTORY ${DAGOR_ENGINE_ROOT}/tools/util
  FILES_CMAKE sbmp2sbp1_files.cmake
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.startup engine.baseUtil engine.math
    tools.libTools.dtx
)
