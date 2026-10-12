set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${CMAKE_CURRENT_SOURCE_DIR})
set(sources blk2sqrat.cpp)

dagor_add_library(gameLibs.dataBlockUtils.blk2sqrat ${sources})
target_include_directories(gameLibs.dataBlockUtils.blk2sqrat PRIVATE ${includes})
target_link_libraries(gameLibs.dataBlockUtils.blk2sqrat PRIVATE Dagor::Quirrel)
