# The compression of vromfs and network data: zlib and zstd. The full set (lz4, snappy, bzip2) needs
# 3rdPartyLibs/arc/snappy-1.1.9 and bzip2-1.0.3, which the fork has not, so this is the minimum set without
# them (DAGOR_MINIMUM_COMPR_UTILS); and the bsdiff tools of the CDK, bsdiffutil and bsapplyutil, which make and apply
# binary patches.
# gameLibs.compressionUtils.wso: the variant for a program that has to make the binary diffs of old clients, whose
# signature offset was wrong (MIMIC_WRONG_SIGNATURE_OFFSET_DIFF_CREATION).
foreach(variant "" .wso)
  set(defines DAGOR_MINIMUM_COMPR_UTILS OPENSSL_SUPPRESS_DEPRECATED)
  if(variant)
    list(APPEND defines MIMIC_WRONG_SIGNATURE_OFFSET_DIFF_CREATION)
  endif()
  dagor_add_target(NAME gameLibs.compressionUtils${variant} STATIC LAX
    FILES_CMAKE compressionUtils_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${DAGOR_PROG_DIR}/gameLibs/publicInclude/compressionUtils ${DAGOR_PROG_DIR}/engine/sharedInclude
      ${DAGOR_PROG_DIR}/tools/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
      ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
    COMPILE_DEFINITIONS PRIVATE ${defines}
    BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.arc.zstd-1.4.5 3rdPartyLibs.bsdiff
      3rdPartyLibs.openssl-3.x.crypto.md5 # the vromfs checks
  )
endforeach()
set(tool_deps engine.osApiWrappers engine.kernel engine.memory engine.coreUtil engine.baseUtil engine.ioSys engine.math
  engine.startup engine.perfMon.daProfilerStub 3rdPartyLibs.arc.zlib-ng 3rdPartyLibs.arc.zstd-1.4.5 3rdPartyLibs.bsdiff
  3rdPartyLibs.openssl-3.x)
if(LINUX)
  list(APPEND tool_deps engine.osApiWrappers.messageBox.stub)
endif()
set(tools bsdiffutil bsapplyutil)
set(kinds DIFF APPLY)
foreach(tool kind IN ZIP_LISTS tools kinds)
  dagor_add_target(NAME ${tool} EXECUTABLE LAX NO_CONFIG_POSTFIX
    FILES_CMAKE bsdiffTools_files.cmake
    INCLUDE_DIRECTORIES PRIVATE
      ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs/publicInclude/compressionUtils
      ${DAGOR_PROG_DIR}/engine/sharedInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
      ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include
    COMPILE_DEFINITIONS PRIVATE DAGOR_MINIMUM_COMPR_UTILS OPENSSL_SUPPRESS_DEPRECATED BSDIFFWRAP_${kind}_EXECUTABLE
    BUILD_DEPENDENCIES PRIVATE ${tool_deps}
    CDK
  )
endforeach()
