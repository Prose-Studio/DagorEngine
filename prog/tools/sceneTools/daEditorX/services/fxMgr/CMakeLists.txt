dagor_add_target(NAME tools.sceneTools.daEditorX.services.fxMgr STATIC LAX
  FILES_CMAKE fxMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.heatHaze
)
