dagor_add_target(NAME list_cpu_features EXECUTABLE LAX
  OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  FILES_CMAKE utils_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${DAGOR_PROG_DIR}/3rdPartyLibs/cpu_features/include
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.cpu_features
)
