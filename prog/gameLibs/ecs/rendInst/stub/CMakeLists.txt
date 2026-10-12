# Stub of the GPU object placing parameters of the ECS rendInst code for programs without it
dagor_add_target(NAME gameLibs.ecs.rendInst.stub STATIC
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
