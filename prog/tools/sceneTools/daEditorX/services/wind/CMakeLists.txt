dagor_add_target(NAME tools.sceneTools.daEditorX.services.wind STATIC LAX
  FILES_CMAKE wind_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
  BUILD_DEPENDENCIES PRIVATE gameLibs.render.wind gameLibs.dataBlockUtils
)
