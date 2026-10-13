dagor_add_target(NAME tools.libTools.meshOptimize STATIC LAX
  FILES_CMAKE meshOptimize_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude/libTools
  COMPILE_DEFINITIONS PRIVATE SAFETY
)
