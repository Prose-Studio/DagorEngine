# Patching of game resource packs (GRP/DxP), vromfs packs and sound banks, reusing unchanged data
set(sources resUpdUtil.cpp)
set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/engine)

dagor_add_library(gameLibs.gameResPatcher LAX ${sources})
target_include_directories(gameLibs.gameResPatcher PRIVATE ${includes})
