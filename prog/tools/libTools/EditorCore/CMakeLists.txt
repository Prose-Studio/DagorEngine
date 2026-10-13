if(NOT WIN32 AND LINUX)
  list(APPEND deps engine.osApiWrappers.linuxGUI)
endif()
set(deps tools.libTools.coolConsole gameLibs.render.fx gameLibs.quirrel.bindQuirrelEx)

dagor_add_target(NAME tools.libTools.EditorCore STATIC LAX
  FILES_CMAKE EditorCore_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
  BUILD_DEPENDENCIES PRIVATE ${deps} Dagor::Quirrel
)
