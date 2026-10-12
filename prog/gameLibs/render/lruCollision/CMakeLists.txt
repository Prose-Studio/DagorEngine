dagor_add_target(NAME gameLibs.render.lruCollision STATIC
  FILES_CMAKE lruCollision_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
