# daScript modules of the games (prog/gameLibs/das/common.jam): pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
dagor_glob_sources(das DIRS . GLOB *.das)
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_library(gameLibs.das.math LAX pull.cpp)
target_compile_definitions(gameLibs.das.math PRIVATE ${defines})
dagor_target_das_aot(gameLibs.das.math PULL math_aot_DAS_pull_AOT ${das})
