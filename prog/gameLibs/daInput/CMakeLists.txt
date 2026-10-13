dagor_add_target(NAME gameLibs.daInput STATIC
  FILES_CMAKE daInput_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/3rdPartyLibs/pcre/pcre ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.eastl
)
