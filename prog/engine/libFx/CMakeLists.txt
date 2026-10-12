# Common effects support: fx texture prefetching for texture streaming and the leaves wind effect
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
set(sources fxTex.cpp leavesWind.cpp)

dagor_add_library(engine.libFx LAX ${sources})
target_include_directories(engine.libFx PRIVATE ${includes})
