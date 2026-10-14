# Jolt's own unit tests (doctest), on the engine's build of Jolt: its settings (Dagor::JoltSettings: cross-platform
# deterministic, the engine's alignment) and floating point math (that of Jolt itself), so what they check is the Jolt
# the games run
set(options)
dagor_deterministic_fp(options KEEP_NANS)
dagor_add_target(NAME joltPhysics-UnitTests EXECUTABLE LAX
  FILES_CMAKE UnitTests_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/.. ${CMAKE_CURRENT_SOURCE_DIR}
  COMPILE_OPTIONS PRIVATE ${options}
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.phys.joltPhysics Dagor::JoltSettings
)
dagor_add_exec_test(3rdPartyLibs.joltPhysics.UnitTests COMMAND $<TARGET_FILE:joltPhysics-UnitTests> TAGS 3rdPartyLibs)
