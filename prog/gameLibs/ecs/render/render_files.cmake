set(FILES animCharUtils.cpp)
set(ES_FILES
  decalsES.cpp.inl
  animCharNodeDebugES.cpp.inl
  animCharParamsDebugES.cpp.inl
  animCharConsoleUtilsES.cpp.inl
  animRandomNodeHiderES.cpp.inl
  tonemapES.cpp.inl
  shaderVarsES.cpp.inl
  resPtrES.cpp.inl
  postfxRendererES.cpp.inl
  RTPoolES.cpp.inl
  shadersES.cpp.inl
  computeShaderES.cpp.inl
  samplerHandleES.cpp.inl
  gpuDeformObjectsES.cpp.inl
  aimRenderES.cpp.inl
)
list(APPEND ES_FILES "$<$<NOT:$<CONFIG:Rel>>:${CMAKE_CURRENT_LIST_DIR}/animCharDbgRenderES.cpp.inl>")
