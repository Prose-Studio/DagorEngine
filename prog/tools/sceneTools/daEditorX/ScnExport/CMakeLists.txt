dagor_add_target(NAME tools.sceneTools.daEditorX.ScnExport STATIC LAX
  FILES_CMAKE ScnExport_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE tools.libTools.csgFaceRemover
)
