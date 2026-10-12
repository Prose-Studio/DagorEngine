# daScript modules of the games (prog/gameLibs/das/common.jam): pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
dagor_glob_sources(das DIRS . GLOB *.das)
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_library(gameLibs.das.ecs LAX pull.cpp)
target_include_directories(gameLibs.das.ecs PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasQuirrel/src)
target_compile_definitions(gameLibs.das.ecs PRIVATE ${defines})
target_link_libraries(gameLibs.das.ecs PRIVATE Dagor::Quirrel)
dagor_target_das_aot(gameLibs.das.ecs PULL ecs_aot_DAS_pull_AOT ${das})
