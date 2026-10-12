set(sources aviWriter.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/engine/sharedInclude)

dagor_add_library(gameLibs.aviWriter ${sources})
target_include_directories(gameLibs.aviWriter PRIVATE ${includes})
