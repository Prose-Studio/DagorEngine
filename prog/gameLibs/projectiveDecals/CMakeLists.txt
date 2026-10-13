dagor_add_target(NAME gameLibs.projectiveDecals STATIC
  FILES_CMAKE projectiveDecals_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  BUILD_DEPENDENCIES PRIVATE engine.lib3d gameLibs.render
)
