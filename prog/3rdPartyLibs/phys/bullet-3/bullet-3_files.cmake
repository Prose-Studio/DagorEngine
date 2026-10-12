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
dagor_glob_sources(FILES DIRS ${dirs} GLOB *.cpp *.c)
