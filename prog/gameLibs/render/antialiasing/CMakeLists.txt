# Ported from prog/gameLibs/render/antialiasing/jamfile (jam2cmake/skeleton.py; the mobile antialiasing of jam's UseMobileAA is not used)
add_subdirectory(stub)

set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources antialiasing.cpp temporalSuperResolution.cpp)

dagor_add_library(gameLibs.render.antialiasing LAX ${sources})
target_include_directories(gameLibs.render.antialiasing PRIVATE ${includes})
