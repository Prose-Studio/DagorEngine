# The physics engine of the tree: Dagor::Phys, which the
# libraries that use it link, carries its definitions, include dir and engine/phys library (engine.phys.physJolt or
# engine.phys.physBullet). DAGOR_PHYS is Jolt, or Bullet in the tool trees.
include_guard(GLOBAL)

add_library(DagorPhys INTERFACE)
add_library(Dagor::Phys ALIAS DagorPhys)
_dagor_configs(_dagor_phys_checked ${DAGOR_CHECKED_CONTAINERS_CONFIGS})
# Jolt's own settings, for Jolt, engine/phys/physJolt and the users of Dagor::Phys
add_library(DagorJoltSettings INTERFACE)
add_library(Dagor::JoltSettings ALIAS DagorJoltSettings)
target_compile_definitions(DagorJoltSettings INTERFACE JPH_CROSS_PLATFORM_DETERMINISTIC JPH_DEFAULT_ALLOCATE_ALIGNMENT=16)
# the asserts and the debug renderer in Dev and Dbg (not under TSan, whose checks they fail)
set(DAGOR_JOLT_DEBUG "$<CONFIG:Dev,Dbg>")
if(DAGOR_SANITIZE STREQUAL "thread")
  set(DAGOR_JOLT_DEBUG 0)
endif()
target_compile_definitions(DagorJoltSettings INTERFACE "$<${DAGOR_JOLT_DEBUG}:JPH_ENABLE_ASSERTS>"
  "$<${DAGOR_JOLT_DEBUG}:JPH_DEBUG_RENDERER>" "$<$<NOT:$<AND:${DAGOR_JOLT_DEBUG},${_dagor_phys_checked}>>:JPH_NO_DEBUG>")
if(DAGOR_ARCH STREQUAL "x86_64" AND DAGOR_SSE EQUAL 4)
  target_compile_definitions(DagorJoltSettings INTERFACE JPH_USE_SSE4_1 JPH_USE_SSE4_2) # SSE4.2 for popcnt
endif()
if(DAGOR_SANITIZE STREQUAL "address")
  target_compile_definitions(DagorJoltSettings INTERFACE JPH_DISABLE_TEMP_ALLOCATOR JPH_DISABLE_CUSTOM_ALLOCATOR)
endif()
if(DAGOR_ARCH STREQUAL "e2k")
  target_compile_options(DagorJoltSettings INTERFACE -w2810)
endif()

# Bullet's own settings, for Bullet, engine/phys/physBullet and the users of Dagor::Phys
add_library(DagorBulletSettings INTERFACE)
add_library(Dagor::BulletSettings ALIAS DagorBulletSettings)
target_include_directories(DagorBulletSettings INTERFACE "${DAGOR_PROG_DIR}/3rdPartyLibs/phys/bullet-3/src")
target_compile_definitions(DagorBulletSettings INTERFACE BT_THREADSAFE "$<${_dagor_phys_checked}:BT_DEBUG>")
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  target_compile_definitions(DagorBulletSettings INTERFACE B3_USE_CLEW)
endif()
if(ANDROID)
  target_compile_definitions(DagorBulletSettings INTERFACE BT_USE_NEON BT_USE_SIMD_VECTOR3 BT_NO_SYSCTL)
endif()

# each engine for the code built on a given one (gameLibs.vehiclePhys.jolt and .bullet), Dagor::Phys the tree's
add_library(DagorPhysJolt INTERFACE)
add_library(Dagor::PhysJolt ALIAS DagorPhysJolt)
target_compile_definitions(DagorPhysJolt INTERFACE USE_JOLT_PHYSICS)
target_include_directories(DagorPhysJolt INTERFACE "${DAGOR_PROG_DIR}/3rdPartyLibs/phys/joltPhysics")
target_link_libraries(DagorPhysJolt INTERFACE Dagor::JoltSettings engine.phys.physJolt)
add_library(DagorPhysBullet INTERFACE)
add_library(Dagor::PhysBullet ALIAS DagorPhysBullet)
target_compile_definitions(DagorPhysBullet INTERFACE USE_BULLET_PHYSICS)
target_link_libraries(DagorPhysBullet INTERFACE Dagor::BulletSettings engine.phys.physBullet)
target_link_libraries(DagorPhys INTERFACE Dagor::Phys${DAGOR_PHYS})
unset(_dagor_phys_checked)
