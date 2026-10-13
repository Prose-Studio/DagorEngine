dagor_add_target(NAME tools.sceneTools.daEditorX.services.skiesSrv STATIC LAX
  FILES_CMAKE skiesSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE gameLibs.daSkies2 gameLibs.dataBlockUtils
)
