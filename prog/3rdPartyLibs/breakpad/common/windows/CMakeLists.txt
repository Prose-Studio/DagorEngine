# Breakpad's common Windows code (string and GUID utilities) for its client
dagor_add_library(3rdPartyLibs.breakpad.common.windows LAX string_utils.cc guid_string.cc)
target_include_directories(3rdPartyLibs.breakpad.common.windows PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/breakpad)
