dagor_add_target(NAME gameLibs.render.psoCacheLoader STATIC
  FILES_CMAKE psoCacheLoader_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
