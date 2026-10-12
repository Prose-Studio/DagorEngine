# daECS bindings of daScript: entity systems, events and queries in scripts
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/engine/dagorInclude
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
)
file(GLOB AllSources RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
set(sources ${AllSources})
if(DAGOR_DAS_LLVM_AOT)
  list(APPEND defines DAS_LLVM_AOT)
endif()
set(SourceDAS ecs.das)
list(APPEND stringify ${SourceDAS})
list(APPEND deps 1stPartyLibs.daScript engine.workCycle)
if(WIN32)
  list(APPEND options /bigobj)
endif()
if(IS_DIRECTORY "${DAGOR_PROG_DIR}/engine/daECS/net")
  list(APPEND defines HAS_DANET)
endif()

dagor_add_library(gameLibs.ecs.scripts.das ${sources})
target_include_directories(gameLibs.ecs.scripts.das PRIVATE ${includes})
target_compile_definitions(gameLibs.ecs.scripts.das PRIVATE ${defines})
target_compile_options(gameLibs.ecs.scripts.das PRIVATE ${options})
target_link_libraries(gameLibs.ecs.scripts.das PRIVATE ${deps})
dagor_target_stringify(gameLibs.ecs.scripts.das ${stringify})
