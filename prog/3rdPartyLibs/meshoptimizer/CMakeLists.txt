# meshoptimizer: vertex cache, overdraw and fetch optimization, simplification
dagor_add_target(NAME 3rdPartyLibs.meshoptimizer STATIC LAX
  FILES_CMAKE meshoptimizer_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/meshoptimizer/include
  COMPILE_DEFINITIONS PRIVATE _RELEASE
)
