# Texture debug viewer (a stub in Rel)
dagor_add_target(NAME gameLibs.render.texDebug STATIC
  FILES_CMAKE texDebug_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
