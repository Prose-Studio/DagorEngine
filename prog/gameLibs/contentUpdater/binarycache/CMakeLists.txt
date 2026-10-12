dagor_add_target(NAME gameLibs.contentUpdater.binarycache STATIC
  FILES_CMAKE binarycache_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
