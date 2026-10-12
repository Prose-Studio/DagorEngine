# Ambient occlusion (SSAO, GTAO, mobile SSAO; a gameLibs module): its users add this dir to their include dirs
dagor_add_dng_module(gameLibs.render.ambientOcclusion CPP_DIRS .)
target_include_directories(gameLibs.render.ambientOcclusion PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
target_link_libraries(gameLibs.render.ambientOcclusion PRIVATE gameLibs.render)
