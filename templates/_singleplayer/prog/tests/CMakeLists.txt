# The game's tests (ctest --preset <host>-client, see <engine>/_docs/source/testing): C++ unit tests, daScript unit
# tests, ECS tests (the game headless where the tree has the stub driver) and scenario tests (they render)
add_subdirectory(cpp)
add_subdirectory(das)
add_subdirectory(ecs)
add_subdirectory(scenarios)
