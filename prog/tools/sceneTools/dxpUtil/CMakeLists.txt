dagor_add_target(NAME dxpRepack EXECUTABLE LAX OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  FILES_CMAKE dxpUtil_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine
  COMPILE_DEFINITIONS PRIVATE _TARGET_DABUILD_STATIC
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.memory.rtl engine.kernel engine.baseUtil engine.ioSys engine.startup engine.math
    engine.gameRes engine.lib3d engine.drv.drv3d_null engine.perfMon.daProfilerStub tools.libTools.util
    tools.libTools.dtx
)
