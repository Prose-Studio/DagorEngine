# Debug mesh coloring stubs for programs without it
dagor_add_target(NAME gameLibs.render.debugMesh.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
