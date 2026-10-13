# Quirrel async runtime per VM: the sqasync binding, the "async" module and its timer queue
dagor_add_target(NAME gameLibs.quirrel.asyncRuntime STATIC
  FILES_CMAKE asyncRuntime_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
    ${DAGOR_PROG_DIR}/engine/sharedInclude
  BUILD_DEPENDENCIES PRIVATE Dagor::Quirrel
)
