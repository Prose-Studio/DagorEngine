# Quirrel bindings of the async HTTP client (responses by callback or through the event bus)
dagor_add_target(NAME gameLibs.quirrel.http STATIC
  FILES_CMAKE http_files.cmake
  INCLUDE_DIRECTORIES PRIVATE
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel ${DAGOR_PROG_DIR}/engine/sharedInclude
    ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  BUILD_DEPENDENCIES PRIVATE
    Dagor::Quirrel gameLibs.quirrel.quirrel_json gameLibs.quirrel.sqEventBus 1stPartyLibs.jsoncpp
)

# its tests: the scripts of tests/ run by csq against a local HTTP server of the runner, their output compared with the
# .expected files
if(DAGOR_ENGINE_TESTS)
  dagor_add_exec_test(gameLibs.quirrel.http COMMAND ${Python3_EXECUTABLE} tests/run_tests.py --csq $<TARGET_FILE:csq>
    TAGS quirrel)
endif()
