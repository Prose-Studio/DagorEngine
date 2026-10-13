if(WIN32)
  list(APPEND options /wd4548)
  list(APPEND defines "$<$<NOT:$<CONFIG:Rel>>:ANIM_PBC_HOT_RELOAD_ENABLED>") # jam had it on Windows only
endif()

dagor_add_target(NAME gameLibs.dasModules.generic STATIC
  FILES_CMAKE generic_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  COMPILE_DEFINITIONS PRIVATE ${defines}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 1stPartyLibs.daScript gameLibs.gameMath Dagor::Phys
)
