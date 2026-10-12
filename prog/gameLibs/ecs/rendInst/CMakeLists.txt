add_subdirectory(stub)
list(APPEND deps 3rdPartyLibs.eastl gameLibs.rendInst)
list(APPEND deps Dagor::Phys)

dagor_add_target(NAME gameLibs.ecs.rendInst STATIC
  FILES_CMAKE rendInst_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
