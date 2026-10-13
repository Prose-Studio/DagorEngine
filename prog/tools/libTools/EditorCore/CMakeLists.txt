# (Windows and Linux; on Linux the programs that use it have the GUI layer of DAGOR_LINUX_GUI)
set(deps tools.libTools.coolConsole gameLibs.render.fx gameLibs.quirrel.bindQuirrelEx)

dagor_add_target(NAME tools.libTools.EditorCore STATIC LAX
  FILES_CMAKE EditorCore_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/1stPartyLibs/quirrel/quirrel/squirrel
  BUILD_DEPENDENCIES PRIVATE ${deps} Dagor::Quirrel
)
