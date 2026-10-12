# daECS game resource stubs for programs without game resources
dagor_add_target(NAME engine.daECS.gameResStub STATIC
  FILES_CMAKE gameResStub_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.daECS.core 3rdPartyLibs.eastl
)
