dagor_add_target(NAME gameLibs.daSDF STATIC
  FILES_CMAKE daSDF_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders
  BUILD_DEPENDENCIES PRIVATE engine.lib3d
)
