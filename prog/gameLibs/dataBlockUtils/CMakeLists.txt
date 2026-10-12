add_subdirectory(blk2sqrat)

set(includes
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${CMAKE_CURRENT_SOURCE_DIR}
)
set(sources interpolateBlk.cpp blk2json.cpp blkUtils.cpp blkIterator.cpp)
list(APPEND deps 1stPartyLibs.jsoncpp)

dagor_add_library(gameLibs.dataBlockUtils ${sources})
target_include_directories(gameLibs.dataBlockUtils PRIVATE ${includes})
target_link_libraries(gameLibs.dataBlockUtils PRIVATE ${deps})
