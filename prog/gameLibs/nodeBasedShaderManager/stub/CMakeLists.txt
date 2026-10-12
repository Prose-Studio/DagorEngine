# Node based shader manager stubs: no scripted shader compilation or loading
dagor_add_target(NAME gameLibs.nodeBasedShaderManager.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
