dagor_add_target(NAME gameLibs.render.groundPhysDetails STATIC
  FILES_CMAKE groundPhysDetails_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render ${CMAKE_CURRENT_SOURCE_DIR}
)
