set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources particlePhys.cpp)
set(deps 3rdPartyLibs.regExp)

dagor_add_library(gameLibs.daPhys ${sources})
target_include_directories(gameLibs.daPhys PRIVATE ${includes})
target_link_libraries(gameLibs.daPhys PRIVATE ${deps})
