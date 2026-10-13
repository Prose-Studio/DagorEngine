dagor_add_target(NAME tools.libTools.staticGeom STATIC LAX
  FILES_CMAKE staticGeom_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE engine.daBVH
)
