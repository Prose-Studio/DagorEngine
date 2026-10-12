# rendInst effects stubs (composite entities, detail fx types) for programs without them
dagor_add_target(NAME gameLibs.rendInst.riFx.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
