set(includes ${DAGOR_PROG_DIR}/gameLibs/publicInclude ${DAGOR_PROG_DIR}/dagorInclude)
set(sources deviceResetTelemetry.cpp)
list(APPEND deps engine.lib3d gameLibs.statsd)

dagor_add_library(gameLibs.render.deviceResetTelemetry ${sources})
target_include_directories(gameLibs.render.deviceResetTelemetry PRIVATE ${includes})
target_link_libraries(gameLibs.render.deviceResetTelemetry PRIVATE ${deps})
