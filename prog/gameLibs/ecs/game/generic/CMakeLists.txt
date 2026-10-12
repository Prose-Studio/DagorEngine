list(APPEND deps 3rdPartyLibs.eastl)
list(APPEND deps Dagor::Phys)

dagor_add_target(NAME gameLibs.ecs.game.generic STATIC
  FILES_CMAKE generic_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel ${deps}
)
