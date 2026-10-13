# the damage model's stub (the fork has no gameLibs/damageModel), with daNetGame's settings
dagor_add_target(NAME daNetGameLibs.dm.stub STATIC LAX
  FILES_CMAKE stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_DNG_INCLUDES}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel Dagor::Phys
)
