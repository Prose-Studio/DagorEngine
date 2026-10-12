# daScript modules of the games (prog/gameLibs/das/common.jam): pull.cpp references them; with DAGOR_DAS_AOT their
# scripts are compiled into the library
set(defines)
if(DAGOR_DAS_AOT)
  set(defines BUILD_AOT_LIB) # pull.cpp then names the AOT pull
endif()
dagor_add_target(NAME gameLibs.das.ecs STATIC LAX
  FILES_CMAKE ecs_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasQuirrel/src
  COMPILE_DEFINITIONS PRIVATE ${defines}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
  DAS_PULL ecs_aot_DAS_pull_AOT
)
