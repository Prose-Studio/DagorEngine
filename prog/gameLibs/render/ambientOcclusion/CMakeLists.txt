# Ambient occlusion (SSAO, GTAO, mobile SSAO; a gameLibs module): its users add this dir to their include dirs
dagor_add_dng_module(ambientOcclusion CPP_DIRS .
  PRIVATE_INCLUDES ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  DEPS gameLibs/render
)
