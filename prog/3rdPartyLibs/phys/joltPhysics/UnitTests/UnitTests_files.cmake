# Jolt's own list (UnitTests.cmake), without the ObjectStream test (ENABLE_OBJECT_STREAM unset): the engine's build of
# Jolt has no JPH_OBJECT_STREAM
set(PHYSICS_REPO_ROOT ${CMAKE_CURRENT_LIST_DIR}/..)
include(${CMAKE_CURRENT_LIST_DIR}/UnitTests.cmake)
set(FILES ${UNIT_TESTS_SRC_FILES})
