# The BLK and image utilities of the CDK, always optimized (so without a config suffix): binBlk converts BLK files
# between text and binary form (in the CDK's default build), blk2robin to read-only binary BLKs, blkDiff (Windows) makes
# the inheritance diff of two BLKs, utf8ranges prints the Unicode ranges of a text, ltout2img and detClientMask turn
# lightmap outputs into images and detail client masks.
set(deps engine.osApiWrappers engine.kernel engine.memory engine.ioSys engine.baseUtil engine.perfMon.daProfilerStub
  tools.libTools.util)
if(LINUX)
  list(APPEND deps engine.osApiWrappers.messageBox.stub)
endif()

dagor_add_target(NAME binBlk EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE binBlk_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
  BUILD_DEPENDENCIES PRIVATE ${deps} 3rdPartyLibs.openssl-3.x
  CDK
)
foreach(tool blk2robin utf8ranges)
  dagor_add_target(NAME ${tool} EXECUTABLE LAX NO_CONFIG_POSTFIX
    FILES_CMAKE ${tool}_files.cmake
    BUILD_DEPENDENCIES PRIVATE ${deps} engine.startup engine.math
    CDK
  )
endforeach()
if(WIN32)
  dagor_add_target(NAME blkDiff EXECUTABLE LAX NO_CONFIG_POSTFIX
    FILES_CMAKE blkDiff_files.cmake
    BUILD_DEPENDENCIES PRIVATE ${deps} engine.startup engine.math
    CDK
  )
endif()
foreach(tool ltout2img detClientMask)
  dagor_add_target(NAME ${tool} EXECUTABLE LAX NO_CONFIG_POSTFIX
    FILES_CMAKE ${tool}_files.cmake
    BUILD_DEPENDENCIES PRIVATE ${deps} engine.startup engine.math engine.image tools.libTools.dtx
    CDK
  )
endforeach()

# the tests of binBlk, blk2robin, blkDiff and detClientMask (tests/, writing into their DAGOR_TEST_OUT): every value
# type survives each binary BLK form (the repo's BLKs too), the JSON export is JSON, an invalid BLK is rejected,
# includes resolve relative to their file, blkDiff's inheritance reads back as the BLK it was made from and a missing
# BLK fails it, the client masks hold the texels of each client's samples. They run in the build dir: a tool that fails
# fatally writes its log there.
if(DAGOR_CDK_TESTS)
  set(expect_exit ${DAGOR_CMAKE_DIR}/scripts/expect_exit.cmake)
  set(common WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  set(blks ${CMAKE_CURRENT_SOURCE_DIR}/tests/all_types.blk ${DAGOR_PROG_DIR}/gameLibs/ecs/dasEcsUnitTest/entities.blk
    ${DAGOR_PROG_DIR}/gameLibs/render/lensFlare/templates/lens_flare.template.blk
    ${DAGOR_PROG_DIR}/tools/dag4blend/dagorShaders.blk)
  set(names binBlk.roundtrip binBlk.roundtrip-packed binBlk.roundtrip-bbf3 blk2robin.roundtrip)
  set(modes binary packed bbf3 robin)
  foreach(name mode IN ZIP_LISTS names modes)
    set(robin)
    if(mode STREQUAL "robin")
      set(robin -DBLK2ROBIN=$<TARGET_FILE:blk2robin>)
    endif()
    dagor_add_exec_test(${name} COMMAND ${CMAKE_COMMAND} -DBINBLK=$<TARGET_FILE:binBlk> ${robin} -DMODE=${mode}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/blk_roundtrip.cmake ${blks} ${common})
  endforeach()
  dagor_add_exec_test(binBlk.json COMMAND ${Python3_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/tests/blk_json.py
    $<TARGET_FILE:binBlk> ${common})
  dagor_add_exec_test(binBlk.invalid COMMAND ${CMAKE_COMMAND} -DCODE=1 -P ${expect_exit} $<TARGET_FILE:binBlk>
    ${CMAKE_CURRENT_SOURCE_DIR}/tests/invalid.blk -v ${common})
  dagor_add_exec_test(binBlk.includes COMMAND ${CMAKE_COMMAND} -DBINBLK=$<TARGET_FILE:binBlk>
    -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/blk_includes.cmake ${common})
  dagor_add_exec_test(blkDiff.inheritance COMMAND ${CMAKE_COMMAND} -DBLKDIFF=$<TARGET_FILE:blkDiff>
    -DBINBLK=$<TARGET_FILE:binBlk> -P ${CMAKE_CURRENT_SOURCE_DIR}/tests/blk_inheritance.cmake PLATFORMS windows
    ${common})
  dagor_add_exec_test(blkDiff.missing COMMAND ${CMAKE_COMMAND} -DCODE=1 -P ${expect_exit} $<TARGET_FILE:blkDiff>
    ${CMAKE_CURRENT_BINARY_DIR}/tests/missing.blk ${CMAKE_CURRENT_SOURCE_DIR}/tests/inherit_child.blk
    ${CMAKE_CURRENT_BINARY_DIR}/tests/missing-diff.blk PLATFORMS windows ${common})
  foreach(scenario masks no-clients)
    dagor_add_exec_test(detClientMask.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/det_client_mask.py ${scenario} $<TARGET_FILE:detClientMask> ${common})
  endforeach()
endif()

# the tests of utf8ranges and ltout2img (tests/<tool>_tests.py): the Unicode pages of texts in several scripts; a
# lightmapper output, written by the test, in each image format, read back by the format's rules
if(DAGOR_CDK_TESTS)
  foreach(scenario ranges errors)
    dagor_add_exec_test(utf8ranges.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/utf8ranges_tests.py ${scenario} $<TARGET_FILE:utf8ranges>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
  foreach(scenario tga pfm hdr errors)
    dagor_add_exec_test(ltout2img.${scenario} COMMAND ${Python3_EXECUTABLE} -B
      ${CMAKE_CURRENT_SOURCE_DIR}/tests/ltout2img_tests.py ${scenario} $<TARGET_FILE:ltout2img>
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk TIMEOUT 60)
  endforeach()
endif()
