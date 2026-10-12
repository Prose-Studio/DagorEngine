# Tools math: k-DOP bounding volumes
set(includes ${DAGOR_PROG_DIR}/tools/sharedInclude)
set(sources kdop.cpp)

dagor_add_library(tools.libTools.math LAX ${sources})
target_include_directories(tools.libTools.math PRIVATE ${includes})
