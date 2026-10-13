# The network relay server of daNet (into the tree's bin)
dagor_add_target(NAME relay EXECUTABLE LAX
  FILES_CMAKE relay_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/enet/include
  BUILD_DEPENDENCIES PRIVATE
    engine.osApiWrappers engine.kernel engine.memory.rtl engine.ioSys engine.startup engine.baseUtil engine.math
    engine.perfMon.daProfilerStub engine.daNet
)
