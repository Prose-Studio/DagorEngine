# Quirrel base64 encoding and decoding module
set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel)
set(deps gameLibs.quirrel.quirrel_json)
set(sources base64.cpp)

dagor_add_library(gameLibs.quirrel.base64 ${sources})
target_include_directories(gameLibs.quirrel.base64 PRIVATE ${includes})
target_link_libraries(gameLibs.quirrel.base64 PRIVATE Dagor::Quirrel ${deps})
