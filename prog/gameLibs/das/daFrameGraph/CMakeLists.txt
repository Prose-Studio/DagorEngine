# daScript modules of the games: pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_target(NAME gameLibs.das.daFrameGraph STATIC LAX
  FILES_CMAKE daFrameGraph_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph
  COMPILE_DEFINITIONS PRIVATE ${defines}
  DAS_PULL daFrameGraph_aot_DAS_pull_AOT
)
