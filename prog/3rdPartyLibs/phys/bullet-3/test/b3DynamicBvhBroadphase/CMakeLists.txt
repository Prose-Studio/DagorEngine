# Bullet 3's dynamic BVH broadphase: the overlap of two proxies
include(../bullet_test.cmake)
bullet_test(NAME bullet-3-b3DynamicBvhBroadphase
  FILES_CMAKE b3DynamicBvhBroadphase_files.cmake
)
dagor_add_exec_test(3rdPartyLibs.bullet-3.b3DynamicBvhBroadphase
  COMMAND $<TARGET_FILE:bullet-3-b3DynamicBvhBroadphase> TAGS 3rdPartyLibs)
# it exits with 0 either way: a failed check prints "<n> tests failed"
if(TEST 3rdPartyLibs.bullet-3.b3DynamicBvhBroadphase)
  set_tests_properties(3rdPartyLibs.bullet-3.b3DynamicBvhBroadphase PROPERTIES FAIL_REGULAR_EXPRESSION "tests failed")
endif()
