dagor_add_target(NAME tools.sceneTools.daEditorX.de3dllCore STATIC LAX
  FILES_CMAKE de3dllCore_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
  BUILD_DEPENDENCIES PRIVATE
    3rdPartyLibs.imgui engine.memory.rtlOverride engine.math engine.drv.drv3d_use_d3di tools.libTools.EditorCore
    tools.libTools.util tools.libTools.ObjectEditor
)
