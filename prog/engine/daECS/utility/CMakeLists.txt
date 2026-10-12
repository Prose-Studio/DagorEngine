# daECS utilities: entity helpers, templates DB, events
dagor_add_target(NAME engine.daECS.utility STATIC
  FILES_CMAKE utility_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/eastl/include
  BUILD_DEPENDENCIES PRIVATE engine.daECS.core
)
