add_subdirectory(weather_effects)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources animCharUtils.cpp)
list(APPEND deps 3rdPartyLibs.eastl gameLibs.resourcePool)
set(SourceES
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
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/ecs/phys" AND IS_DIRECTORY "${DAGOR_PROG_DIR}/gameLibs/gamePhys/ballistics")
  list(APPEND defines HAS_ECS_PHYS)
endif()
list(APPEND SourceES "$<$<NOT:$<CONFIG:Rel>>:${CMAKE_CURRENT_SOURCE_DIR}/animCharDbgRenderES.cpp.inl>")
list(APPEND deps Dagor::Phys)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.render ${sources})
target_include_directories(gameLibs.ecs.render PRIVATE ${includes})
target_compile_definitions(gameLibs.ecs.render PRIVATE ${defines})
target_link_libraries(gameLibs.ecs.render PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.render ${es_sources})
