# Quirrel async runtime per VM: the sqasync binding, the "async" module and its timer queue
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/engine/sharedInclude
)
set(sources asyncRuntimeBindings.cpp)

dagor_add_library(gameLibs.quirrel.asyncRuntime ${sources})
target_include_directories(gameLibs.quirrel.asyncRuntime PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.asyncRuntime PRIVATE Dagor::Quirrel)
