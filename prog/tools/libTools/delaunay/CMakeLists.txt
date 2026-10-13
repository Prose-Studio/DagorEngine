dagor_add_target(NAME tools.libTools.delaunay STATIC LAX
  FILES_CMAKE delaunay_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/tools/sharedInclude/libTools ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  COMPILE_DEFINITIONS PRIVATE SAFETY
  COMPILE_OPTIONS PRIVATE -FIdelmem.h
)
