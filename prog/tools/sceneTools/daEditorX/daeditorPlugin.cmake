# daeditor_plugin(NAME <name> <dagor_add_target arguments>): a plugin of daEditor3x in plugins/daEditorX of the tools
# (jam's plugin_setup.jam), on daKernel and the editor's core (de3dllCore); included by the plugins' directories
include_guard(GLOBAL)
function(daeditor_plugin)
  dagor_add_target(${ARGN} SHARED LAX OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin/plugins/daEditorX
    CDK_SUBDIR plugins/daEditorX
    INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include
    BUILD_DEPENDENCIES PRIVATE tools.sceneTools.daEditorX.de3dllCore tools.libTools.daKernel
    PROPERTIES DAGOR_LINUX_GUI ON
  )
endfunction()
