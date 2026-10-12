set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
set(sources propsStub.cpp)

dagor_add_library(gameLibs.gamePhys.props.stub ${sources})
target_include_directories(gameLibs.gamePhys.props.stub PRIVATE ${includes})
