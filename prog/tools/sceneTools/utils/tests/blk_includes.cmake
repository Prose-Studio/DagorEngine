# cmake -DBINBLK=<binBlk> -P blk_includes.cmake (in DAGOR_TEST_OUT)
# binBlk -final (includes resolved) run in the test's dir, not where the BLK is: include_main.blk includes
# include/part.blk, which includes base.blk next to it, each relative to the file that includes it (as DataBlock::load
# resolves them), and must read as include_expected.blk.
include("${CMAKE_CURRENT_LIST_DIR}/blk_check.cmake")
if(NOT BINBLK)
  message(FATAL_ERROR "usage: cmake -DBINBLK=<binBlk> -P blk_includes.cmake")
endif()
blk_test_out()
run("${BINBLK}" "${CMAKE_CURRENT_LIST_DIR}/include_main.blk" "${OUT}/resolved.blk" -t -final -h)
run("${BINBLK}" "${CMAKE_CURRENT_LIST_DIR}/include_expected.blk" "${OUT}/expected.blk" -t -h)
check_same_text("${OUT}/expected.blk" "${OUT}/resolved.blk")
