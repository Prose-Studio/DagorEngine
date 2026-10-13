dagor_add_target(NAME tools.sceneTools.daEditorX.services.dngBasedRenderSrv STATIC LAX
  FILES_CMAKE dngBasedRenderSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api
)
