# The d3d:: functions as calls through the driver's interface table (d3di), for code that a program with the driver
# loads (the editors' plugins); in a multi-driver tree only those the headers do not make inline (d3d_wrap.cpp)
dagor_add_target(NAME engine.drv.drv3d_use_d3di STATIC LAX
  FILES_CMAKE drv3d_use_d3di_files.cmake
)
