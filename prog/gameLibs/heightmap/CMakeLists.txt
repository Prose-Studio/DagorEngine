# Heightmaps: compressed height data, their LOD grid rendering and queries; tool builds (DAGOR_BUILDING_TOOLS) keep
# the editing data
set(defines)
if(DAGOR_BUILDING_TOOLS)
  set(defines _TARGET_PC_TOOLS_BUILD)
endif()

dagor_add_target(NAME gameLibs.heightmap STATIC LAX
  FILES_CMAKE heightmap_files.cmake
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE engine.heightMapLand gameLibs.frustumCulling
)
