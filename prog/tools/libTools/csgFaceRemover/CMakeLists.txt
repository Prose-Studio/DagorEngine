dagor_add_target(NAME tools.libTools.csgFaceRemover STATIC LAX
  FILES_CMAKE csgFaceRemover_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/math/carve/include
  COMPILE_DEFINITIONS PRIVATE NDEBUG CARVE_NODEBUG CARVE_USE_EXACT_PREDICATES
  BUILD_DEPENDENCIES PRIVATE tools.libTools.staticGeom engine.daBVH 3rdPartyLibs.math.carve
)
