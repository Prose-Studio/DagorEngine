dagor_add_target(NAME gameLibs.daEditorE STATIC LAX
  FILES_CMAKE daEditorE_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel tools.libTools.util gameLibs.quirrel.sqEventBus gameLibs.quirrel.frp gameLibs.quirrel.quirrel_json
)
