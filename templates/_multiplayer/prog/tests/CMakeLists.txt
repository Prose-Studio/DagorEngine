# The game's tests (ctest --preset <host>-dedicated and <host>-client, see <engine>/_docs/source/testing): C++ unit
# tests, daScript unit tests and ECS tests in the dedicated server's tree, scenario tests (they render) in the client's
if(DAGOR_DEDICATED)
  add_subdirectory(cpp)
  add_subdirectory(das)
  add_subdirectory(ecs)
else()
  add_subdirectory(scenarios)
  add_subdirectory(editor)
endif()
