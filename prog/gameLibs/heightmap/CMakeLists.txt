# Heightmaps: compressed height data, their LOD grid rendering and queries; tool builds (DAGOR_BUILDING_TOOLS) keep
# the editing data
set(sources
  heightmapCompressError.cpp
  lodGridVertexData.cpp
  simpleHeightmapRenderer.cpp
  heightmapRenderer.cpp
  heightmapPhysHandler.cpp
  heightmapMaxDelta.cpp
  heightmapMetricsCalc.cpp
  heightmapMetricsCulling.cpp
  heightmapCulling.cpp
  heightmapLoader.cpp
  heightmapHandler.cpp
  riverMasks/hmapCriticalPath.cpp
  riverMasks/hmapLodMaskBuild.cpp
)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps engine.heightMapLand gameLibs.frustumCulling)
set(defines)
if(DAGOR_BUILDING_TOOLS)
  set(defines _TARGET_PC_TOOLS_BUILD)
endif()

dagor_add_library(gameLibs.heightmap LAX ${sources})
target_include_directories(gameLibs.heightmap PRIVATE ${includes})
target_compile_definitions(gameLibs.heightmap PRIVATE ${defines})
target_link_libraries(gameLibs.heightmap PRIVATE ${deps})
