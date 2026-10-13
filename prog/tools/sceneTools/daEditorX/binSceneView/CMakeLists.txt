dagor_add_target(NAME tools.sceneTools.daEditorX.binSceneView STATIC LAX
  FILES_CMAKE binSceneView_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.pathFinder gameLibs.pathFinder.tileCache.stub gameLibs.pathFinder.customNav.stub gameLibs.covers
    engine.shaders
)
