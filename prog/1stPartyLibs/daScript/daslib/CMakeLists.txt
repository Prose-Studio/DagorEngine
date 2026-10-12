# daScript's standard library scripts compiled ahead of time (DAGOR_DAS_AOT), which 1stPartyLibs/daScript links then
dagor_add_target(NAME 1stPartyLibs.daScript.daslib STATIC LAX
  FILES_CMAKE daslib_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  LICENSES ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/LICENSE
  DAS_PULL daslib_DAS_pull_AOT
)
