dagor_add_dng_module(NAME daNetGameLibs.package_physobj DAS
  FILES_CMAKE package_physobj_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/daNetGameLibs
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.gamePhys.phys.physObj
  PULL_VARS turretControl
)
