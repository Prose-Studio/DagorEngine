dagor_add_target(NAME tools.libTools.scriptPanelWrapper STATIC LAX
  FILES_CMAKE scriptPanelWrapper_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE engine.coreUtil gameLibs.quirrel.bindQuirrelEx Dagor::Quirrel
)
