dagor_add_dng_module(NAME gameLibs.render.collimatorMoaCore DAS
  FILES_CMAKE collimatorMoaCore_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/gameLibs
)
