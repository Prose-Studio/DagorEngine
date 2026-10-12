# ARM's ASTC encoder: the astcenc programs (one per instruction set; one universal binary on macOS) that the texture
# exporter runs.
#   Astcenc::Astcenc  the programs that link it get the astcenc programs two dirs above them (the root of the CDK, where
#                     the exporter plugins look for them)
# Astcenc_ROOT: a local copy (default: the pinned one, fetched).
include(DagorFetch)
dagor_sdk_root(Astcenc astcenc)
file(GLOB Astcenc_PROGRAMS "${Astcenc_ROOT}/astcenc*")
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Astcenc REQUIRED_VARS Astcenc_PROGRAMS)
if(Astcenc_FOUND AND NOT TARGET Astcenc::Astcenc)
  add_library(Astcenc::Astcenc INTERFACE IMPORTED GLOBAL)
  set(_programs ${Astcenc_PROGRAMS})
  list(TRANSFORM _programs PREPEND "../..|")
  set_target_properties(Astcenc::Astcenc PROPERTIES TRANSITIVE_LINK_PROPERTIES DAGOR_RUNTIME_FILES
    INTERFACE_DAGOR_RUNTIME_FILES "${_programs}")
  unset(_programs)
endif()
