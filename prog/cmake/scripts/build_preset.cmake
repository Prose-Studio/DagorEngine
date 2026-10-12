# cmake -DSOURCE_DIR=<dir with CMakePresets.json> -DPRESET=<preset> [-DTARGETS=<target>,...] [-DCOMPONENT=<component>]
#       -P build_preset.cmake
# Builds another tree a build step needs (the engine's host tools, a game's daScript AOT compiler): configures PRESET
# once (its tree <SOURCE_DIR>/../build/<PRESET>, the one cmake --preset makes), builds it in Dev (only TARGETS when
# given) and installs COMPONENT of it. A lock keeps the trees that share it from building it at the same time.
foreach(var SOURCE_DIR PRESET)
  if(NOT ${var})
    message(FATAL_ERROR "build_preset.cmake: ${var} is not set")
  endif()
endforeach()
cmake_path(ABSOLUTE_PATH SOURCE_DIR NORMALIZE)
cmake_path(GET SOURCE_DIR PARENT_PATH root)
set(tree "${root}/build/${PRESET}")
file(MAKE_DIRECTORY "${root}/build")
file(LOCK "${tree}.lock" TIMEOUT 14400 RESULT_VARIABLE locked)
if(locked)
  message(FATAL_ERROR "Cannot lock ${tree}.lock: ${locked}")
endif()

if(NOT EXISTS "${tree}/CMakeCache.txt")
  execute_process(COMMAND "${CMAKE_COMMAND}" --preset ${PRESET} WORKING_DIRECTORY "${SOURCE_DIR}" COMMAND_ERROR_IS_FATAL ANY)
endif()
set(targets)
if(TARGETS)
  string(REPLACE "," ";" targets "${TARGETS}")
  list(PREPEND targets --target)
endif()
execute_process(COMMAND "${CMAKE_COMMAND}" --build "${tree}" --config Dev ${targets} COMMAND_ERROR_IS_FATAL ANY)
if(COMPONENT)
  execute_process(COMMAND "${CMAKE_COMMAND}" --install "${tree}" --config Dev --component ${COMPONENT}
    COMMAND_ERROR_IS_FATAL ANY)
endif()
