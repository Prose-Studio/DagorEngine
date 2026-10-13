# The games' sound on FMOD Studio (DAGOR_GAME_SOUND): events, banks, streams, mixing, occlusion; its debug views outside
# Rel. Without the FMOD Studio API (FindFMOD.cmake) there is only the stub.
find_package(FMOD QUIET)
if(NOT FMOD_FOUND)
  return()
endif()
dagor_add_target(NAME gameLibs.soundSystem STATIC
  FILES_CMAKE soundSystem_files.cmake
  COMPILE_OPTIONS PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/wd4505> # the unused FMOD_ErrorString of fmod_errors.h
  BUILD_DEPENDENCIES PUBLIC FMOD::Studio PRIVATE engine.coreUtil gameLibs.soundOcclusionGPU
)
