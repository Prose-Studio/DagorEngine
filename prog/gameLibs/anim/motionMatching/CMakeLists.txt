dagor_add_dng_module(NAME gameLibs.anim.motionMatching DAS
  FILES_CMAKE motionMatching_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR} ${DAGOR_PROG_DIR}/gameLibs ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/3rdPartyLibs/acl/includes
  BUILD_DEPENDENCIES PRIVATE Dagor::Phys
  PULL_VARS mmEvents
)
