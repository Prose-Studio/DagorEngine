dagor_add_target(NAME 3rdPartyLibs.codecs.libogg-1.1.3 STATIC LAX
  FILES_CMAKE libogg-1.1.3_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ../include
)

# libogg's self-tests of its bit packer and its framing (_V_SELFTEST); the framing one runs only as a program: it memcmp's
# whole ogg_packet structs, padding included, which optimized builds leave uninitialized
if(DAGOR_ENGINE_TESTS)
  foreach(name bitwise framing)
    set(ogg_source src/${name}.c)
    dagor_add_target(NAME libogg-1.1.3-${name} EXECUTABLE LAX
      FILES_CMAKE ogg_test_files.cmake
      INCLUDE_DIRECTORIES PRIVATE ../include
      COMPILE_DEFINITIONS PRIVATE _V_SELFTEST
      BUILD_DEPENDENCIES PRIVATE engine.memory.minrtl # libogg allocates with the engine's memalloc
    )
  endforeach()
  dagor_add_exec_test(3rdPartyLibs.libogg.bitwise COMMAND $<TARGET_FILE:libogg-1.1.3-bitwise> TAGS 3rdPartyLibs)
endif()
