set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include)
set(AllSrcFolder_CPP .)
dagor_glob_sources(sources DIRS ${AllSrcFolder_CPP} GLOB *.cpp)
set(deps gameLibs.sepClient)

dagor_add_library(gameLibs.sepClientInstance ${sources})
target_include_directories(gameLibs.sepClientInstance PRIVATE ${includes})
target_link_libraries(gameLibs.sepClientInstance PRIVATE ${deps})
