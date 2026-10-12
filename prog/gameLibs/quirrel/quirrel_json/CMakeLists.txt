# JSON for Quirrel: conversion to and from jsoncpp and rapidjson, a direct JSON parser and writer
dagor_add_target(NAME gameLibs.quirrel.quirrel_json STATIC
  FILES_CMAKE quirrel_json_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 1stPartyLibs.jsoncpp 3rdPartyLibs.arc.zstd-1.4.5
)
