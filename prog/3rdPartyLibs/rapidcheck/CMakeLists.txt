dagor_add_target(NAME 3rdPartyLibs.rapidcheck STATIC LAX
  FILES_CMAKE rapidcheck_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidcheck/include
  PROPERTIES DAGOR_RTTI ON
)
