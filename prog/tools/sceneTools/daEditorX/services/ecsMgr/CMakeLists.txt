dagor_add_target(NAME tools.sceneTools.daEditorX.services.ecsMgr STATIC LAX
  FILES_CMAKE ecsMgr_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE
    engine.daECS.io.datablock engine.daECS.core engine.daECS.utility gameLibs.ecs.render gameLibs.ecs.anim
    gameLibs.render.daFrameGraph gameLibs.render.resourceSlot
)
