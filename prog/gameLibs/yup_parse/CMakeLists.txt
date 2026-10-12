# Reading .yup files: bencoded dictionaries queried by '/' separated key paths
set(includes
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/3rdPartyLibs/bencode
  ${DAGOR_PROG_DIR}/engine/dagorInclude
)
set(sources yup.cpp)
list(APPEND deps 3rdPartyLibs.bencode)

dagor_add_library(gameLibs.yup_parse ${sources})
target_include_directories(gameLibs.yup_parse PRIVATE ${includes})
target_link_libraries(gameLibs.yup_parse PRIVATE ${deps})
