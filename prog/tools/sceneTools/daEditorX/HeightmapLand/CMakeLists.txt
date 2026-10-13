# The daEditor3x plugins of heightmaps and land meshes: heightmapLand and heightmapLand-aces (the ACES heightmap and land
# mesh: USE_HMAP_ACES, USE_LMESH_ACES, with the land normals' rendering)
include(../daeditorPlugin.cmake)
set(includes
  ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Recast/Include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  # propPanel's private curve math (CubicPolynomCB, CubicPSplineCB) for the curve samplers of the typed variables
  ${DAGOR_PROG_DIR}/tools/libTools/propPanel/commonWindow
)
set(deps
  tools.libTools.assetMgr tools.libTools.delaunay tools.libTools.winGuiWrapper tools.libTools.propPanel
  tools.libTools.staticGeom tools.libTools.dagFileRW gameLibs.landMesh engine.daBVH engine.image
  engine.perfMon.daProfilerStub 3rdPartyLibs.math.DelaunayTriangulator 3rdPartyLibs.math.clipper-4.x
  3rdPartyLibs.math.misc 3rdPartyLibs.hash 3rdPartyLibs.image.tiff-4.4.0 3rdPartyLibs.recastnavigation.Recast
  3rdPartyLibs.recastnavigation.Detour 3rdPartyLibs.recastnavigation.DetourTileCache gameLibs.pathFinder
  gameLibs.pathFinder.tileCache.stub gameLibs.pathFinder.customNav.stub gameLibs.recastTools gameLibs.covers
  gameLibs.physMap
)
daeditor_plugin(NAME heightmapLand
  FILES_CMAKE heightmapLand_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
daeditor_plugin(NAME heightmapLand-aces
  FILES_CMAKE heightmapLand_files.cmake heightmapLand-aces_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE USE_HMAP_ACES USE_LMESH_ACES
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
