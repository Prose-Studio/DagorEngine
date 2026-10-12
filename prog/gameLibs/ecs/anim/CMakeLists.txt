set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps 3rdPartyLibs.eastl gameLibs.render.animCharTexReplace)
set(SourceES
  animChar.cpp.inl
  slotAttachES.cpp.inl
  animStateES.cpp.inl
  animIrqES.cpp.inl
  randomAnimStarterES.cpp.inl
  animCharEffectorsES.cpp.inl
)
set(sources animUtils.cpp)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.anim ${sources})
target_include_directories(gameLibs.ecs.anim PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.anim PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.anim ${es_sources})
