# TODO(jam): ToolsHaveVR ?= no ;
dagor_add_target(NAME tools.sceneTools.daEditorX.services.dynRenderSrv STATIC LAX
  FILES_CMAKE dynRenderSrv_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/render/screenSpaceReflection
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.render.upscale gameLibs.render.specialVision gameLibs.render.genericLUT gameLibs.vr
)
