set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources curveEditorJsPlugin.cpp)
set(SourceJS curveEditor.js)
list(APPEND stringify ${SourceJS})

dagor_add_library(gameLibs.webui.plugins.editorCurves ${sources})
target_include_directories(gameLibs.webui.plugins.editorCurves PRIVATE ${includes})
dagor_target_stringify(gameLibs.webui.plugins.editorCurves ${stringify})
