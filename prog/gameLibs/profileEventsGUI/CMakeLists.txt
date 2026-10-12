set(includes ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
list(APPEND deps 3rdPartyLibs.eastl)
set(sources profileEventsGUI.cpp)

dagor_add_library(gameLibs.profileEventsGUI ${sources})
target_include_directories(gameLibs.profileEventsGUI PRIVATE ${includes})
target_link_libraries(gameLibs.profileEventsGUI PRIVATE ${deps})
