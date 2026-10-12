# Bullet 3 (https://github.com/bulletphysics/bullet3, rev 39b8de74df93721add193e5b3d9ebee579faebf8), the physics of the
# tools (DAGOR_PHYS Bullet): its collision, dynamics and soft bodies, the world importer, and OpenCL (through clew) on
# the desktops and Android. It builds with Dagor::BulletSettings, as its users do (DagorPhys.cmake).
set(dirs
  src # btBulletCollisionAll.cpp, btBulletDynamicsAll.cpp, btLinearMathAll.cpp
  src/Bullet3Collision/BroadPhaseCollision
  src/Bullet3Collision/NarrowPhaseCollision
  src/Bullet3Common
  src/Bullet3Dynamics
  src/Bullet3Dynamics/ConstraintSolver
  src/Bullet3Geometry
  src/BulletInverseDynamics
  src/BulletInverseDynamics/details
  src/BulletSoftBody
  src/BulletSoftBody/BulletReducedDeformableBody
  Extras/Serialize/BulletWorldImporter
  Extras/Serialize/BulletFileLoader
)
if(CMAKE_SYSTEM_NAME MATCHES "^(Windows|Darwin|Linux|Android)$")
  list(APPEND dirs src/Bullet3OpenCL/BroadphaseCollision src/Bullet3OpenCL/Initialize
    src/Bullet3OpenCL/NarrowphaseCollision src/Bullet3OpenCL/ParallelPrimitives src/Bullet3OpenCL/Raycast
    src/Bullet3OpenCL/RigidBody src/clew)
endif()
dagor_glob_sources(sources DIRS ${dirs} GLOB *.cpp *.c)

dagor_add_library(3rdPartyLibs.phys.bullet-3 LAX ${sources})
target_link_libraries(3rdPartyLibs.phys.bullet-3 PUBLIC Dagor::BulletSettings)
if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  target_link_libraries(3rdPartyLibs.phys.bullet-3 PUBLIC "$<LINK_LIBRARY:FRAMEWORK,OpenCL>")
endif()
if(WIN32)
  target_compile_definitions(3rdPartyLibs.phys.bullet-3 PRIVATE _CRT_SECURE_NO_WARNINGS _CRT_SECURE_NO_DEPRECATE
    _SCL_SECURE_NO_WARNINGS)
endif()
# its results do not depend on the compiler's floating point contractions (no FMA, no unsafe math)
set(options)
if(MSVC AND CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  list(APPEND options -fp:fast)
  if(DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND options /clang:-fno-unsafe-math-optimizations /clang:-mno-fma)
  endif()
  list(APPEND options -Wno-unknown-warning-option -Wno-single-bit-bitfield-constant-conversion)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  list(APPEND options /wd4267)
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  list(APPEND options -ffast-math -Wno-unused-parameter -Wno-uninitialized)
  if(DAGOR_ARCH STREQUAL "x86_64")
    list(APPEND options -fno-unsafe-math-optimizations -mno-fma)
  endif()
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    list(APPEND options -Wno-macro-redefined -Wno-unknown-warning-option -Wno-single-bit-bitfield-constant-conversion)
  endif()
endif()
target_compile_options(3rdPartyLibs.phys.bullet-3 PRIVATE ${options})
