dagor_add_dng_module(NAME daNetGameLibs.sound.door_sounds DAS
  FILES_CMAKE door_sounds_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/daNetGame ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  BUILD_DEPENDENCIES PRIVATE daNetGameLibs.sound.sound_utils
)
