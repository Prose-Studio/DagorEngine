# The Quirrel bindings of the games' sound (soundSystem)
find_package(FMOD QUIET)
if(NOT FMOD_FOUND)
  return()
endif()
dagor_add_target(NAME gameLibs.soundSystem.quirrel STATIC
  FILES_CMAKE quirrel_files.cmake
  BUILD_DEPENDENCIES PRIVATE gameLibs.soundSystem gameLibs.quirrel.bindQuirrelEx Dagor::Quirrel
)
