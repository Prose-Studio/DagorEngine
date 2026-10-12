dagor_add_target(NAME gameLibs.daGI2 STATIC
  FILES_CMAKE daGI2_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR} shaders
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.daSDF
)
