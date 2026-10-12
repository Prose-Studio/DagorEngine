# Metronome: frame pacing measurements on top of daFrameGraph
dagor_add_target(NAME gameLibs.render.metronome STATIC
  FILES_CMAKE metronome_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR}
)
