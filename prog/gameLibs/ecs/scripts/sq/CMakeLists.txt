dagor_add_target(NAME gameLibs.ecs.scripts.sq STATIC
  FILES_CMAKE sq_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.quirrel.quirrel_json
)
