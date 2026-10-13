# Program startup helpers (message box crash report on Windows)
if(DAGOR_KERNEL_LINKAGE STREQUAL "dynamic")
  set(deps engine.memory.rtlOverride)
endif()
list(APPEND deps 3rdPartyLibs.eastl)

dagor_add_target(NAME engine.startup STATIC LAX
  FILES_CMAKE startup_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs
  BUILD_DEPENDENCIES PRIVATE ${deps}
)
