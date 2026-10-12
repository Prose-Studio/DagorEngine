if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  list(APPEND options -Wno-deprecated-declarations)
endif()

dagor_add_target(NAME 1stPartyLibs.daScript.modules.dasQuirrel STATIC
  FILES_CMAKE dasQuirrel_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel 3rdPartyLibs.eastl 1stPartyLibs.daScript
)
