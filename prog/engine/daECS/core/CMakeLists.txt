# daECS: entities, components, templates, systems, events
if(NOT DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.baseUtil)
endif()
list(APPEND deps 3rdPartyLibs.eastl 3rdPartyLibs.regExp)

dagor_add_target(NAME engine.daECS.core STATIC
  FILES_CMAKE core_files.cmake
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
