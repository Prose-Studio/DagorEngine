dagor_add_target(NAME gameLibs.render.terraform STATIC
  FILES_CMAKE terraform_files.cmake
  INCLUDE_DIRECTORIES PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
