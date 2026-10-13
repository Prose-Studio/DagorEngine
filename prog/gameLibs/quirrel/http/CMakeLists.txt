# Quirrel bindings of the async HTTP client (responses by callback or through the event bus)
dagor_add_target(NAME gameLibs.quirrel.http STATIC
  FILES_CMAKE http_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel gameLibs.quirrel.quirrel_json gameLibs.quirrel.sqEventBus 1stPartyLibs.jsoncpp
)
