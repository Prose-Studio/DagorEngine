# cmake -DBLKDIFF=<blkDiff> -DBINBLK=<binBlk> -P blk_inheritance.cmake (in DAGOR_TEST_OUT)
# blkDiff writes inherit_child.blk as an include of inherit_parent.blk and the differences (@override:, @delete:, new
# params and blocks, at the top level and in blocks). The diff must leave out what both have, include the parent by its
# path relative to the diff (given absolute paths, and relative ones from another dir), and binBlk -final (includes and
# directives resolved) must read it as the child.
include("${CMAKE_CURRENT_LIST_DIR}/blk_check.cmake")
if(NOT BLKDIFF OR NOT BINBLK)
  message(FATAL_ERROR "usage: cmake -DBLKDIFF=<blkDiff> -DBINBLK=<binBlk> -P blk_inheritance.cmake")
endif()
blk_test_out()
set(parent "${CMAKE_CURRENT_LIST_DIR}/inherit_parent.blk")
set(child "${CMAKE_CURRENT_LIST_DIR}/inherit_child.blk")
run("${BINBLK}" "${child}" "${OUT}/child.blk" -t -h)

# the diff of the BLKs given by absolute paths, and of copies given by paths relative to the dir it runs in
file(COPY "${parent}" "${child}" DESTINATION "${OUT}/src")
file(MAKE_DIRECTORY "${OUT}/rel")
foreach(case "absolute|${parent}|${child}|${OUT}/diff.blk|[^\n]*/inherit_parent\\.blk"
    "relative|src/inherit_parent.blk|src/inherit_child.blk|rel/diff.blk|\\.\\./src/inherit_parent\\.blk")
  string(REPLACE "|" ";" case "${case}")
  list(GET case 0 name)
  list(GET case 1 parent_arg)
  list(GET case 2 child_arg)
  list(GET case 3 diff_arg)
  list(GET case 4 include_re)
  run("${BLKDIFF}" "${parent_arg}" "${child_arg}" "${diff_arg}")
  cmake_path(ABSOLUTE_PATH diff_arg BASE_DIRECTORY "${OUT}" OUTPUT_VARIABLE diff_fn)
  file(READ "${diff_fn}" diff)
  if(NOT diff MATCHES "^include \"${include_re}\"\n")
    message(FATAL_ERROR "${diff_fn} (${name} paths) does not start with the include of the parent:\n${diff}")
  endif()
  if(diff MATCHES "untouched")
    message(FATAL_ERROR "${diff_fn} repeats what the parent and the child have in common:\n${diff}")
  endif()
  run("${BINBLK}" "${diff_fn}" "${OUT}/resolved-${name}.blk" -t -final -h)
  check_same_text("${OUT}/child.blk" "${OUT}/resolved-${name}.blk")
endforeach()
