set(FILES nodeBasedShaderManager.cpp)
# the shaders' compilation where the games have webui on Windows, the stub elsewhere
set(compile 0)
if(WIN32 AND DEFINED DAGOR_GAME_WEBUI AND DAGOR_VARIANT STREQUAL "game")
  set(compile "${DAGOR_GAME_WEBUI}")
endif()
set(dir ${CMAKE_CURRENT_LIST_DIR})
list(APPEND FILES "$<IF:${compile},${dir}/nodeBasedShaderManagerCompile.cpp,${dir}/stub/nodeBasedShaderManagerCompileStub.cpp>")
