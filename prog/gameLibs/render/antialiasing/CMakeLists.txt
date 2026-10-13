# Ported from prog/gameLibs/render/antialiasing/jamfile (jam2cmake/skeleton.py; the mobile antialiasing of jam's UseMobileAA is not used)
dagor_add_target(NAME gameLibs.render.antialiasing STATIC LAX
  FILES_CMAKE antialiasing_files.cmake
)
