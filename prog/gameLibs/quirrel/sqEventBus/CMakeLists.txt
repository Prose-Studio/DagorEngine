# Quirrel event bus: events between VMs and native code, the eventbus module
dagor_add_target(NAME gameLibs.quirrel.sqEventBus STATIC
  FILES_CMAKE sqEventBus_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.quirrel.sqCrossCall
)
