dagor_add_target(NAME tools.sceneTools.pointCloudGen.generator STATIC
  FILES_CMAKE generator_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/sharedInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE
    gameLibs.rendInst gameLibs.landMesh engine.daECS.core gameLibs.ecs.gameres gameLibs.render gameLibs.gamePhys.phys
    gameLibs.gamePhys.collision.customRendinstTrace gameLibs.gamePhys.collision.collision-common tools.libTools.assetMgr
    tools.libTools.dagFileRW
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
