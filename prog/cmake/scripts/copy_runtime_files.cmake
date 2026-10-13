# cmake -DLIST=<file> -DDEST=<dir> -P copy_runtime_files.cmake
# Copies the runtime files a program needs next to it (dagor_target_runtime_files): LIST has one "<subdir>|<file>" per
# line (the program's DAGOR_RUNTIME_FILES), copied into DEST/<subdir> when they changed.
file(STRINGS "${LIST}" entries)
foreach(entry IN LISTS entries)
  if(NOT entry MATCHES "^([^|]*)[|](.+)$")
    continue()
  endif()
  set(dir "${DEST}/${CMAKE_MATCH_1}")
  set(file "${CMAKE_MATCH_2}")
  if(NOT EXISTS "${file}")
    message(FATAL_ERROR "Runtime file ${file} does not exist")
  endif()
  cmake_path(GET file FILENAME name)
  file(MAKE_DIRECTORY "${dir}")
  file(COPY_FILE "${file}" "${dir}/${name}" ONLY_IF_DIFFERENT INPUT_MAY_BE_RECENT)
endforeach()
