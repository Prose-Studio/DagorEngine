# The web UI's node-based shader editors (environment cover, fog, clouds). The comp variant: the compile-only build of the
# node-based shader compiler (NBSM_COMPILE_ONLY).
add_subdirectory(stub)

foreach(variant "" .comp)
  set(name gameLibs.webui.plugins.shaderEditors${variant})
  dagor_add_library(${name} shaderEditors.cpp enviCoverShaderEditor.cpp fogShaderEditor.cpp cloudsShaderEditor.cpp)
  target_include_directories(${name} PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
endforeach()
target_compile_definitions(gameLibs.webui.plugins.shaderEditors.comp PRIVATE NBSM_COMPILE_ONLY)
