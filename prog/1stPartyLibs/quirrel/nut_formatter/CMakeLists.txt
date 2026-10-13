dagor_add_target(NAME nut_formatter EXECUTABLE LAX
  FILES_CMAKE nut_formatter_files.cmake
  COMPILE_DEFINITIONS PRIVATE __B_NO_MEM_BASE_INCLUDE
  CDK
)
