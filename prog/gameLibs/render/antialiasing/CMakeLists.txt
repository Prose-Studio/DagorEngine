# Temporal antialiasing and the upscalers (the mobile antialiasing is not used)
dagor_add_target(NAME gameLibs.render.antialiasing STATIC LAX
  FILES_CMAKE antialiasing_files.cmake
)
