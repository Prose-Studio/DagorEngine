# Reading .yup files: bencoded dictionaries queried by '/' separated key paths
dagor_add_target(NAME gameLibs.yup_parse STATIC
  FILES_CMAKE yup_parse_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/3rdPartyLibs/bencode
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.bencode
)
