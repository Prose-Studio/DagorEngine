set(includes ${DAGOR_PROG_DIR}/dagorInclude)
set(sources animCharStub.cpp)

dagor_add_library(engine.animChar.stub ${sources})
target_include_directories(engine.animChar.stub PRIVATE ${includes})
