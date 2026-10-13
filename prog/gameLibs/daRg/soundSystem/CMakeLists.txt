# The UI sounds of daRg on the games' sound (soundSystem)
find_package(FMOD QUIET)
if(NOT FMOD_FOUND)
  return()
endif()
dagor_add_target(NAME gameLibs.daRg.soundSystem STATIC
  FILES_CMAKE soundSystem_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE gameLibs.soundSystem gameLibs.soundSystem.quirrel Dagor::Quirrel
)
