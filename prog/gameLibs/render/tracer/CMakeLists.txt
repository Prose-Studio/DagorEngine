dagor_add_target(NAME gameLibs.render.tracer STATIC
  FILES_CMAKE tracer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
