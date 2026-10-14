# FlatBuffers: the library, and its schema compiler flatc and flathash (the hashes of names), console tools of the CDK.
# They are standalone (only flatc links the library): the C runtime's operator new, not the engine's allocator, which
# GCC would inline into them (dag_memBase.h) without the engine's memory to link.
dagor_add_target(NAME 3rdPartyLibs.flatbuffers STATIC LAX
  FILES_CMAKE flatbuffers_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
)
dagor_add_target(NAME flatc EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE flatc_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include grpc
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.flatbuffers
  CDK
)
dagor_add_target(NAME flathash EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE flathash_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  CDK
)

# the tests of flatc and flathash (tests/flatbuffers_tools.py, writing into their DAGOR_TEST_OUT): JSON compiled to a
# binary and back, the C++ the engine keeps generated from its schemas, the hashes of names
if(DAGOR_CDK_TESTS)
  set(names flatc.json flatc.cpp flathash.fnv)
  set(scenarios json cpp hash)
  foreach(name scenario IN ZIP_LISTS names scenarios)
    dagor_add_exec_test(${name} COMMAND ${Python3_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/tests/flatbuffers_tools.py
      ${scenario} $<TARGET_FILE:flatc> $<TARGET_FILE:flathash> WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} TAGS cdk
      TIMEOUT 60)
  endforeach()
endif()
