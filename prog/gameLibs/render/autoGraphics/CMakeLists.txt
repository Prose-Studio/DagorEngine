dagor_add_target(NAME gameLibs.render.autoGraphics STATIC
  FILES_CMAKE autoGraphics_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
  PROPERTIES DAGOR_FRAME_LIMIT 262144
)
