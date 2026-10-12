# Collision export helpers: export node types by name, V-HACD mesh face checks and fixes
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(sources exportCollisionNodeType.cpp vhacdMeshChecker.cpp)

dagor_add_library(tools.libTools.collision LAX ${sources})
target_include_directories(tools.libTools.collision PRIVATE ${includes})
