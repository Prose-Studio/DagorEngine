dagor_add_target(NAME gameLibs.ecs.scripts.dasSq STATIC
  FILES_CMAKE dasSq_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel gameLibs.quirrel.quirrel_json gameLibs.ecs.scripts.sq gameLibs.ecs.scripts.das
    gameLibs.quirrel.bindQuirrelEx
)
