# Pools of reusable GPU resources and aliasable managed 2D textures
dagor_add_target(NAME gameLibs.resourcePool STATIC
  FILES_CMAKE resourcePool_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
