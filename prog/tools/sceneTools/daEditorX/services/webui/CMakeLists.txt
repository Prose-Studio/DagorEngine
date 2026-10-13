dagor_add_target(NAME tools.sceneTools.daEditorX.services.webui STATIC LAX
  FILES_CMAKE webui_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.webui gameLibs.webui.plugins.ecsviewer gameLibs.webui.plugins.webView gameLibs.webui.websocket
    gameLibs.ecs.scripts.sq
)
