dagor_add_dng_module(NAME daNetGameLibs.zone_force_field
  FILES_CMAKE zone_force_field_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame
)
