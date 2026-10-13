dagor_add_target(NAME gameLibs.render.occlusion STATIC
  FILES_CMAKE occlusion_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
