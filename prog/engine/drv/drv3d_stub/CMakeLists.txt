# The stub 3d driver: the whole driver interface without a GPU (tools, servers, the render tests without a GPU)
set(options)
if(MSVC)
  set(options /FId3d_config.h)
else()
  set(options "SHELL:-include ${CMAKE_CURRENT_SOURCE_DIR}/d3d_config.h")
endif()
dagor_add_target(NAME engine.drv.drv3d_stub STATIC
  FILES_CMAKE drv3d_stub_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/engine/drv/drv3d_commonCode .
  COMPILE_DEFINITIONS PRIVATE D3DSTUBBED INSIDE_DRIVER
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE engine.drv.drv3d_commonCode
)
