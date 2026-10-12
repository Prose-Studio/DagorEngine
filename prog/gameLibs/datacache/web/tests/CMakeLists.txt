# Data cache web backend unit tests (against a local HTTP server)
list(APPEND includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng)
list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/openssl-3.x/include)

dagor_add_catch2_test(NAME datacacheWeb-tests LAX
  TAGS gameLibs net REQUIRES http_server
  FILES_CMAKE tests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${includes}
  COMPILE_DEFINITIONS PRIVATE OPENSSL_SUPPRESS_DEPRECATED
  BUILD_DEPENDENCIES PRIVATE
    engine.memory engine.kernel engine.osApiWrappers engine.baseUtil engine.ioSys engine.math engine.coreUtil
    engine.startup engine.perfMon.daProfilerStub gameLibs.datacache.web 3rdPartyLibs.arc.zlib-ng
)
