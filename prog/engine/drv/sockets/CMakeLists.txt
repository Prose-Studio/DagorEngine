dagor_add_target(NAME engine.drv.sockets STATIC LAX
  FILES_CMAKE sockets_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_NET_CORE
)
