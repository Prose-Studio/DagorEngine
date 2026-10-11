# the damage model's stub (the fork has no gameLibs/damageModel), with daNetGame's settings (jam: setup.jam)
dagor_add_library(QUIRREL SOURCES dm_dng_stub.cpp PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_DNG_INCLUDES}
  DEPS Dagor::Phys)
