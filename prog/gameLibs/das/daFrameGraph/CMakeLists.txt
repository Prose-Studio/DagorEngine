# daScript modules of the games (prog/gameLibs/das/common.jam): pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
dagor_glob_sources(das DIRS . GLOB *.das)
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_library(gameLibs.das.daFrameGraph LAX pull.cpp)
target_include_directories(gameLibs.das.daFrameGraph PRIVATE ${DAGOR_PROG_DIR}/gameLibs/render/daFrameGraph)
target_compile_definitions(gameLibs.das.daFrameGraph PRIVATE ${defines})
dagor_target_das_aot(gameLibs.das.daFrameGraph PULL daFrameGraph_aot_DAS_pull_AOT ${das})
