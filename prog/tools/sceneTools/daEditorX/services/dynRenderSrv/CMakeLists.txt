# The dynamic render service of the editors. The programs with VR (DAGOR_VR: AssetViewer) get the build with its VR
# GUI (TOOLS_HAVE_VR, on AssetViewer's skies service); see dagor_add_link_choice().
foreach(build standard vr)
  set(defines)
  if(build STREQUAL "vr")
    set(defines TOOLS_HAVE_VR)
  endif()
  dagor_add_target(NAME tools.sceneTools.daEditorX.services.dynRenderSrv.${build} STATIC LAX
    FILES_CMAKE dynRenderSrv_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${DAGOR_PROG_DIR}/tools/sceneTools/daEditorX/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude
      ${DAGOR_PROG_DIR}/gameLibs/render/screenSpaceReflection
    COMPILE_DEFINITIONS PRIVATE ${defines}
    BUILD_DEPENDENCIES PRIVATE
      gameLibs.render.ambientOcclusion gameLibs.render.upscale gameLibs.render.specialVision gameLibs.render.genericLUT
      gameLibs.vr
  )
endforeach()
dagor_add_link_choice(tools.sceneTools.daEditorX.services.dynRenderSrv PROPERTY DAGOR_VR
  ON tools.sceneTools.daEditorX.services.dynRenderSrv.vr OFF tools.sceneTools.daEditorX.services.dynRenderSrv.standard)
