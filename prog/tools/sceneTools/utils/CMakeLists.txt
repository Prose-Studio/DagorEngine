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
