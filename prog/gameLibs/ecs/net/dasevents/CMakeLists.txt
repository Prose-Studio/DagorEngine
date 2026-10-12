set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include)
dagor_glob_sources(sources DIRS . GLOB *.cpp)
set(SourceES dasEventES.cpp.inl)
list(APPEND es_sources ${SourceES})

dagor_add_library(gameLibs.ecs.net.dasevents ${sources})
target_include_directories(gameLibs.ecs.net.dasevents PRIVATE ${includes})
target_link_libraries(gameLibs.ecs.net.dasevents PRIVATE Dagor::Quirrel)
dagor_target_es_sources(gameLibs.ecs.net.dasevents ${es_sources})
