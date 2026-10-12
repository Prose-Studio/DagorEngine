# The camera manager (a gameLibs module, its pull framework_cameraManager_pull): with the renderer only, without it
# games link gameLibs/cameraManager/stub
add_subdirectory(stub)

set(cpp_dirs)
set(deps)
if(DAGOR_GAME_RENDERER)
  set(cpp_dirs .)
  set(deps gameLibs.folders)
endif()
dagor_add_dng_module(gameLibs.cameraManager CPP_DIRS ${cpp_dirs})
target_include_directories(gameLibs.cameraManager PRIVATE ${DAGOR_PROG_DIR}/gameLibs
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(gameLibs.cameraManager PRIVATE ${deps})
