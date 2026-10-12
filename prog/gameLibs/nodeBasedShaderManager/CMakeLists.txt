add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources nodeBasedShaderManager.cpp)
# the shaders' compilation where the games have webui on Windows (prog/daNetGame/setup.jam), the stub elsewhere
set(compile 0)
if(WIN32 AND DEFINED DAGOR_GAME_WEBUI AND DAGOR_VARIANT STREQUAL "game")
  set(compile "${DAGOR_GAME_WEBUI}")
endif()
set(dir ${CMAKE_CURRENT_SOURCE_DIR})
list(APPEND sources "$<IF:${compile},${dir}/nodeBasedShaderManagerCompile.cpp,${dir}/stub/nodeBasedShaderManagerCompileStub.cpp>")

dagor_add_library(gameLibs.nodeBasedShaderManager ${sources})
target_include_directories(gameLibs.nodeBasedShaderManager PRIVATE ${includes})
