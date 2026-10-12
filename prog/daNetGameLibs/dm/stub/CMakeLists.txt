# the damage model's stub (the fork has no gameLibs/damageModel), with daNetGame's settings (jam: setup.jam)
dagor_add_library(daNetGameLibs.dm.stub LAX dm_dng_stub.cpp)
target_include_directories(daNetGameLibs.dm.stub PRIVATE ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_DNG_INCLUDES})
target_link_libraries(daNetGameLibs.dm.stub PRIVATE Dagor::Quirrel Dagor::Phys)
