# clew, Bullet's loader of the OpenCL runtime: loads and unloads it when there is one, and passes without one
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-clew
  FILES_CMAKE clew_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/phys/bullet-3/src/clew
)
dagor_add_exec_test(3rdPartyLibs.bullet-3.clew COMMAND $<TARGET_FILE:bullet-3-clew> TAGS 3rdPartyLibs)
