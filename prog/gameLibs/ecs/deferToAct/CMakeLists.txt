dagor_add_target(NAME gameLibs.ecs.deferToAct STATIC
  FILES_CMAKE deferToAct_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/engine/dagorInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.eastl
)
