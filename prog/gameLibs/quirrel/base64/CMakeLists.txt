# Quirrel base64 encoding and decoding module
dagor_add_target(NAME gameLibs.quirrel.base64 STATIC
  FILES_CMAKE base64_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel gameLibs.quirrel.quirrel_json
)
