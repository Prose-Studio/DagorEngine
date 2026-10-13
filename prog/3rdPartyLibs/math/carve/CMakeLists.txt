# Carve: CSG on polyhedra (with exact predicates)
set(options)
if(MSVC AND DAGOR_ARCH STREQUAL "x86_64")
  set(options -wd4267) # no support for > 4G vertices
endif()
dagor_add_target(NAME 3rdPartyLibs.math.carve STATIC LAX
  FILES_CMAKE carve_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  COMPILE_DEFINITIONS PRIVATE HAVE_CONFIG_H NDEBUG CARVE_NODEBUG CARVE_USE_EXACT_PREDICATES $<$<BOOL:${WIN32}>:WIN32>
  COMPILE_OPTIONS PRIVATE ${options}
)
