# Unit tests of the raytraced toroidal static shadow's core (scheduler, transforms)
dagor_add_catch2_test(NAME rtss-core-tests LAX
  TAGS gameLibs render
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render/raytracedToroidalStaticShadow
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math
    engine.perfMon.daProfilerStub 3rdPartyLibs.eastl
)
