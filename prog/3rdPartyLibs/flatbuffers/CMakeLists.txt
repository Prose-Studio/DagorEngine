# FlatBuffers: the library, and its schema compiler flatc and flathash (the hashes of names), console tools of the CDK
dagor_add_target(NAME 3rdPartyLibs.flatbuffers STATIC LAX
  FILES_CMAKE flatbuffers_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
)
dagor_add_target(NAME flatc EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE flatc_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include grpc
  BUILD_DEPENDENCIES PRIVATE 3rdPartyLibs.flatbuffers
  CDK
)
dagor_add_target(NAME flathash EXECUTABLE LAX NO_CONFIG_POSTFIX
  FILES_CMAKE flathash_files.cmake
  INCLUDE_DIRECTORIES PRIVATE include
  CDK
)
