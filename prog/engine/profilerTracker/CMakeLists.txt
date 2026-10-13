# Profiler tracker API (a stub: the tracker itself is not part of the engine)
dagor_add_target(NAME engine.profilerTracker STATIC LAX
  FILES_CMAKE profilerTracker_files.cmake
  INCLUDE_DIRECTORIES PRIVATE .
)
