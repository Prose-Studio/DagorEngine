# Every tree of a host and toolchain: the <host>[-<compiler>|-<arch>] presets of prog/CMakePresets.json (cmake --workflow
# --preset windows on a fresh clone). The tree builds the trees of DAGOR_ALL_PRESETS one after the other, each with its
# own preset (scripts/build_preset.cmake: configured once, built in Dev), and installs those of DAGOR_ALL_INSTALL (the
# CDK, the asset build and the editors into tools/). Their configure fetches the pinned SDKs into DAGOR_DEPS_DIR.
include_guard(GLOBAL)

set(DAGOR_ALL_PRESETS "" CACHE STRING "The presets of the trees this tree builds, in order")
set(DAGOR_ALL_INSTALL "" CACHE STRING "Those of DAGOR_ALL_PRESETS whose trees are installed")
set(previous)
foreach(preset IN LISTS DAGOR_ALL_PRESETS)
  set(install)
  if(preset IN_LIST DAGOR_ALL_INSTALL)
    set(install -DINSTALL=ON)
  endif()
  add_custom_target(${preset} ALL
    COMMAND "${CMAKE_COMMAND}" -DSOURCE_DIR=${CMAKE_SOURCE_DIR} -DPRESET=${preset} ${install}
      -P "${CMAKE_CURRENT_LIST_DIR}/scripts/build_preset.cmake"
    COMMENT "The tree of preset ${preset}"
    USES_TERMINAL
    VERBATIM)
  if(previous) # one after the other, in the order of the list: each tree uses every core
    add_dependencies(${preset} ${previous})
  endif()
  set(previous ${preset})
endforeach()
