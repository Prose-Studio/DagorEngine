set(includes
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/engine/sharedInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
set(sources netPhysResync.cpp collRes.cpp collResFromEcs.cpp collResFromRI.cpp)
list(APPEND deps 3rdPartyLibs.eastl)
set(SourceES
  animCharFastPhysDebug.cpp.inl
  particlePhysSys.cpp
  animPhysES.cpp.inl
  animCharFastPhysES.cpp.inl
  physBodyES.cpp.inl
  ragdollES.cpp.inl
  physVarsES.cpp.inl
  gravityES.cpp.inl
  segHumanPhysES.cpp.inl
  turretControlES.cpp.inl
)
list(APPEND deps Dagor::Phys)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.phys ${sources})
target_include_directories(gameLibs.ecs.phys PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.phys PRIVATE ${deps})
dagor_target_es_sources(gameLibs.ecs.phys ${es_sources})
