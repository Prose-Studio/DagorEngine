list(APPEND deps engine.daNet engine.crypto 3rdPartyLibs.arc.lz4)
list(APPEND deps engine.daECS.io.datablock engine.daECS.core 3rdPartyLibs.eastl)

dagor_add_target(NAME engine.daECS.net STATIC
  FILES_CMAKE net_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/enet/include ${DAGOR_PROG_DIR}/3rdPartyLibs/arc
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
