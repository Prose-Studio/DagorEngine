dagor_add_target(NAME 3rdPartyLibs.reachability STATIC LAX
  FILES_CMAKE reachability_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/reachability/include
  COMPILE_OPTIONS PRIVATE -F SystemConfiguration
)
