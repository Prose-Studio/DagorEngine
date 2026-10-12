# Core utilities: simple parameter blocks, base64, localization tables, fly mode
set(sources simplePBlock.cpp base64.cpp localization.cpp)
if(NOT ANDROID OR TRUE)
  list(APPEND sources flyMode.cpp)
endif()
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(deps 3rdPartyLibs.eastl)

dagor_add_library(engine.coreUtil ${sources})
target_include_directories(engine.coreUtil PRIVATE ${includes})
target_link_libraries(engine.coreUtil PRIVATE ${deps})
