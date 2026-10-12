set(FILES
  landMicroDetails.cpp
  lmeshManager.cpp
  lmeshWeightAtlas.cpp
  lmeshWeightAtlasGpu.cpp
  lmeshWeightAtlasLegacyCpu.cpp
  lmeshWeightAtlasLegacyGpu.cpp
  lmeshLandClasses.cpp
  lmeshRenderer.cpp
  lmeshRenderingModeState.cpp
  lmeshRendererLandClasses.cpp
  virtualtexture.cpp
  landRayTracerSoA4.cpp
  lmeshRendererGlue.cpp
  lastClip.cpp
  biomeQuery.cpp
  heightmapQuery.cpp
  lmeshMirroring.cpp
  lmeshHoles.cpp
)
set(dir "${CMAKE_CURRENT_LIST_DIR}")
list(APPEND FILES "$<IF:${debug},${dir}/clipmapDebug.cpp,${dir}/clipmapDebugStub.cpp>")
