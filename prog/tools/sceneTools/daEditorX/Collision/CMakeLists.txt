dagor_add_target(NAME tools.sceneTools.daEditorX.Collision STATIC LAX
  FILES_CMAKE Collision_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/engine/sharedInclude
)
