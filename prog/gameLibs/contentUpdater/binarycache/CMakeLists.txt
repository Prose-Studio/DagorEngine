set(sources binaryCache.cpp)
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)

dagor_add_library(gameLibs.contentUpdater.binarycache ${sources})
target_include_directories(gameLibs.contentUpdater.binarycache PRIVATE ${includes})
target_link_libraries(gameLibs.contentUpdater.binarycache PRIVATE Dagor::Quirrel)
