# Texture debug viewer (a stub in Rel)
dagor_add_library(gameLibs.render.texDebug
  "$<IF:$<CONFIG:Rel>,${CMAKE_CURRENT_SOURCE_DIR}/texDebug_stub.cpp,${CMAKE_CURRENT_SOURCE_DIR}/texDebug.cpp>")
target_include_directories(gameLibs.render.texDebug PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
