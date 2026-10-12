dagor_add_target(NAME gameLibs.ecs.net.dasevents STATIC
  FILES_CMAKE dasevents_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
