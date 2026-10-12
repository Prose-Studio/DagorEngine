# Ported from prog/gameLibs/render/antialiasing/jamfile (jam2cmake/skeleton.py; the mobile antialiasing of jam's UseMobileAA is not used)
add_subdirectory(stub)

dagor_add_target(NAME gameLibs.render.antialiasing STATIC LAX
  FILES_CMAKE antialiasing_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/gameLibs/publicInclude
)
