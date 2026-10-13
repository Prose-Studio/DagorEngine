dagor_add_target(NAME gameLibs.movie STATIC
  FILES_CMAKE movie_files.cmake
  BUILD_DEPENDENCIES PRIVATE engine.videoPlayer 3rdPartyLibs.codecs.libogg-1.1.3 3rdPartyLibs.codecs.libtheora-1.0
)
