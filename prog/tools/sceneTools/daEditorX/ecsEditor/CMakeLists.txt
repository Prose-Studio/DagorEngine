dagor_add_target(NAME tools.sceneTools.daEditorX.ecsEditor STATIC LAX
  FILES_CMAKE ecsEditor_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE tools.libTools.ObjectEditor tools.libTools.ecsPropPanel
)
