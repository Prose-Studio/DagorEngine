# The web UI's node-based shader editors (environment cover, fog, clouds). The comp variant: the compile-only build of the
# node-based shader compiler (NBSM_COMPILE_ONLY).
foreach(variant "" .comp)
  set(name gameLibs.webui.plugins.shaderEditors${variant})
  dagor_add_target(NAME ${name} STATIC
    FILES_CMAKE shaderEditors_files.cmake
  )
endforeach()
target_compile_definitions(gameLibs.webui.plugins.shaderEditors.comp PRIVATE NBSM_COMPILE_ONLY)
