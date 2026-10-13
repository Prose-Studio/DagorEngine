dagor_add_dng_module(NAME daNetGameLibs.burnt_ground.editor_stub
  MODULE_NAME burnt_ground_editor_stub # its pull: framework_burnt_ground_editor_stub_pull
  FILES_CMAKE editor_stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
