dagor_add_target(NAME engine.daECS.delayedAct STATIC
  FILES_CMAKE delayedAct_files.cmake
)
# the pull of its entity system (actInThread_pull)
_dagor_pull_file(engine.daECS.delayedAct "${CMAKE_CURRENT_BINARY_DIR}/gen/delayedAct_es_pull.cpp" ECS actInThread_pull
  actInThread)
