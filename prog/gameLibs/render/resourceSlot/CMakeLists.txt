set(includes
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${CMAKE_CURRENT_SOURCE_DIR}
)
set(sources
  detail/storage.cpp
  detail/unregisterAccess.cpp
  nodeHandleWithSlotsAccess.cpp
  registerAccess.cpp
  resolveAccess.cpp
  state.cpp
  actions.cpp
  das/resourceSlotCoreModule.cpp
  das/registerAccess.cpp
  das/state.cpp
  das/clearResourceSlot.cpp
  das/actionList.cpp
)

dagor_add_library(gameLibs.render.resourceSlot ${sources})
target_include_directories(gameLibs.render.resourceSlot PRIVATE ${includes})
