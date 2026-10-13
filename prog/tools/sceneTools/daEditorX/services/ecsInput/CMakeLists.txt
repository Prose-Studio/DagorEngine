dagor_add_target(NAME tools.sceneTools.daEditorX.services.ecsInput STATIC LAX
  FILES_CMAKE ecsInput_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
