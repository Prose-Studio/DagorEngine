# Unit test support of <unittest/dag_testEnv.h>: test environment, reference images
dagor_add_target(NAME engine.unitTest STATIC
  FILES_CMAKE unitTest_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.image
)
