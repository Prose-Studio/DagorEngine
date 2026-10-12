# Targets of the engine and of projects. dagor_add_library() and dagor_add_executable() are add_library() and
# add_executable() with the engine's defaults; everything else about a target is said with CMake's own commands
# (target_sources, target_include_directories, target_link_libraries, target_compile_definitions, ...) and the
# dagor_target_*() functions of the other modules (generated sources, daScript AOT, licenses, runtime files).
#
#   dagor_add_library(<name> [STATIC|OBJECT|INTERFACE|SHARED|MODULE] [LAX] [OUTPUT_NAME <name>]
#                     [OUTPUT_DIRECTORY <dir>] [NO_CONFIG_POSTFIX] [<source>...])
#   dagor_add_executable(<name> [WIN32] [MACOSX_BUNDLE] [LAX] [OUTPUT_NAME <name>] [OUTPUT_DIRECTORY <dir>]
#                        [NO_CONFIG_POSTFIX] [<source>...])
#
# Targets are named after their directory under prog/, '/' as '.' (prog/engine/math: engine.math), and linked by those
# names. The defaults:
#   - the warnings of first-party code, as errors with DAGOR_WARNINGS_AS_ERRORS; LAX gives third-party code (and
#     first-party code that is not warning-free yet) the lax set instead (DagorCompilerFlags.cmake)
#   - libraries are built for the programs that link them (EXCLUDE_FROM_ALL, unless DAGOR_BUILD_ALL); the engine's
#     programs are built by default when the tree's variant names them (dagor_build_by_default), a project's always
#   - programs and shared libraries are named <name>[-asan|-ubsan|...][-cov]-<config> as jam named them (no suffix in Rel,
#     or with NO_CONFIG_POSTFIX), in OUTPUT_DIRECTORY (default <build>/bin) for every configuration; next to them, the
#     runtime files of the libraries they link (dagor_target_runtime_files) and LICENSE-<file name> with the licenses of
#     those libraries (DagorLicenses.cmake)
#   - an IDE folder after the directory
include_guard(GLOBAL)

# dagor_add_library(<name> ...): see the top
function(dagor_add_library name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "STATIC;OBJECT;INTERFACE;SHARED;MODULE;LAX;NO_CONFIG_POSTFIX"
                        "OUTPUT_NAME;OUTPUT_DIRECTORY" "")
  set(type STATIC)
  foreach(t OBJECT INTERFACE SHARED MODULE)
    if(arg_${t})
      set(type ${t})
    endif()
  endforeach()
  add_library(${name} ${type} ${arg_UNPARSED_ARGUMENTS})
  _dagor_target_defaults(${name})
  if(type MATCHES "^(STATIC|OBJECT)$" AND NOT DAGOR_BUILD_ALL)
    set_property(TARGET ${name} PROPERTY EXCLUDE_FROM_ALL ON)
  endif()
  if(type MATCHES "^(SHARED|MODULE)$")
    set_property(TARGET ${name} PROPERTY DEFINE_SYMBOL "") # no <target>_EXPORTS: the sources say what they export
    _dagor_program_defaults(${name})
  endif()
endfunction()

# dagor_add_executable(<name> ...): see the top
function(dagor_add_executable name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "WIN32;MACOSX_BUNDLE;LAX;NO_CONFIG_POSTFIX" "OUTPUT_NAME;OUTPUT_DIRECTORY" "")
  set(kind)
  if(arg_WIN32)
    list(APPEND kind WIN32)
  endif()
  if(arg_MACOSX_BUNDLE)
    list(APPEND kind MACOSX_BUNDLE)
  endif()
  add_executable(${name} ${kind} ${arg_UNPARSED_ARGUMENTS})
  _dagor_target_defaults(${name})
  _dagor_program_defaults(${name})
  # the engine's programs are made by the variants that want them (prog/CMakeLists.txt), a project's by default
  cmake_path(IS_PREFIX DAGOR_PROG_DIR "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE in_engine)
  if(in_engine AND NOT DAGOR_BUILD_ALL)
    set_property(TARGET ${name} PROPERTY EXCLUDE_FROM_ALL ON)
  endif()
endfunction()

# dagor_build_by_default(<target>...): the targets are part of the tree's default build (cmake --build)
function(dagor_build_by_default)
  foreach(target IN LISTS ARGN)
    if(NOT TARGET ${target})
      message(FATAL_ERROR "dagor_build_by_default: there is no target ${target}")
    endif()
    set_property(TARGET ${target} PROPERTY EXCLUDE_FROM_ALL OFF)
  endforeach()
endfunction()

# the defaults of every target (the calling function's arg_LAX)
macro(_dagor_target_defaults target)
  set_property(TARGET ${target} APPEND PROPERTY TRANSITIVE_LINK_PROPERTIES DAGOR_LICENSE_FILES DAGOR_RUNTIME_FILES
    DAGOR_GAME_PULLS)
  get_property(_dagor_type TARGET ${target} PROPERTY TYPE)
  if(NOT _dagor_type STREQUAL "EXECUTABLE") # a program's own licenses are not listed in its LICENSE file, as in jam
    _dagor_dir_licenses(_dagor_licenses)
    set_property(TARGET ${target} APPEND PROPERTY INTERFACE_DAGOR_LICENSE_FILES ${_dagor_licenses})
  endif()
  if(NOT _dagor_type STREQUAL "INTERFACE_LIBRARY")
    if(arg_LAX)
      target_compile_options(${target} PRIVATE ${DAGOR_LAX_OPTIONS})
    else()
      target_compile_options(${target} PRIVATE ${DAGOR_STRICT_OPTIONS})
      if(DAGOR_WARNINGS_AS_ERRORS)
        set_property(TARGET ${target} PROPERTY COMPILE_WARNING_AS_ERROR ON)
      endif()
    endif()
    _dagor_folder(_dagor_folder)
    set_property(TARGET ${target} PROPERTY FOLDER "${_dagor_folder}")
    # the assembler of a source by its extension, as jam chose it (CMake's own mapping lets MASM claim .asm)
    get_property(_dagor_sources TARGET ${target} PROPERTY SOURCES)
    foreach(_dagor_source IN LISTS _dagor_sources)
      if(_dagor_source MATCHES "\\.(asm|nasm|nas)$")
        set_property(SOURCE "${_dagor_source}" PROPERTY LANGUAGE ASM_NASM)
      elseif(_dagor_source MATCHES "\\.masm$")
        set_property(SOURCE "${_dagor_source}" PROPERTY LANGUAGE ASM_MASM)
      elseif(_dagor_source MATCHES "\\.[sS]$")
        set_property(SOURCE "${_dagor_source}" PROPERTY LANGUAGE ASM)
      endif()
    endforeach()
  endif()
endmacro()

# the IDE folder of the calling directory's targets: its parent's path under prog/ (or under the project)
function(_dagor_folder out)
  cmake_path(IS_PREFIX DAGOR_PROG_DIR "${CMAKE_CURRENT_SOURCE_DIR}" NORMALIZE in_engine)
  if(in_engine)
    cmake_path(RELATIVE_PATH CMAKE_CURRENT_SOURCE_DIR BASE_DIRECTORY "${DAGOR_PROG_DIR}" OUTPUT_VARIABLE rel)
  else()
    cmake_path(RELATIVE_PATH CMAKE_CURRENT_SOURCE_DIR BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" OUTPUT_VARIABLE rel)
    set(rel "${PROJECT_NAME}/${rel}")
  endif()
  cmake_path(GET rel PARENT_PATH folder)
  set(${out} "${folder}" PARENT_SCOPE)
endfunction()

# programs and shared libraries: name, output dir, build stamp, runtime files, license (the calling function's arg_*)
macro(_dagor_program_defaults target)
  set(_dagor_name "${target}")
  if(arg_OUTPUT_NAME)
    set(_dagor_name "${arg_OUTPUT_NAME}")
  endif()
  set(_dagor_san_address asan)
  set(_dagor_san_undefined ubsan)
  set(_dagor_san_thread tsan)
  set(_dagor_san_leak lsan)
  set(_dagor_san_memory msan)
  if(NOT DAGOR_SANITIZE STREQUAL "none")
    string(APPEND _dagor_name "-${_dagor_san_${DAGOR_SANITIZE}}")
  endif()
  if(DAGOR_COVERAGE)
    string(APPEND _dagor_name "-cov")
  endif()
  set_property(TARGET ${target} PROPERTY OUTPUT_NAME "${_dagor_name}")
  if(NOT arg_NO_CONFIG_POSTFIX)
    set_target_properties(${target} PROPERTIES DEV_POSTFIX -dev IREL_POSTFIX -irel DBG_POSTFIX -dbg)
  endif()
  set(_dagor_dir "${CMAKE_BINARY_DIR}/bin")
  if(arg_OUTPUT_DIRECTORY)
    cmake_path(ABSOLUTE_PATH arg_OUTPUT_DIRECTORY NORMALIZE OUTPUT_VARIABLE _dagor_dir)
  endif()
  dagor_set_output_directory(${target} "${_dagor_dir}")
  target_link_libraries(${target} PRIVATE dagor.buildStamp)
  _dagor_program_files(${target})
endmacro()

# dagor_set_output_directory(<target> <dir>): the program or shared library goes to <dir> in every configuration (their
# names differ by the config postfix); $<1:> keeps CMake from adding a per-config subdir
function(dagor_set_output_directory target dir)
  set_target_properties(${target} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "$<1:${dir}>"
    LIBRARY_OUTPUT_DIRECTORY "$<1:${dir}>"
    PDB_OUTPUT_DIRECTORY "$<1:${dir}>")
endfunction()

# dagor_target_runtime_files(<target> [SUBDIR <dir>] <file>...): files a program loads at run time (an SDK's DLLs, say),
# copied next to it after each build (into <dir> there) and installed with it. For a library, every program that links
# it gets them (jam's BundleCopy of a driver's SDK DLLs).
function(dagor_target_runtime_files target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "SUBDIR" "")
  set(subdir ".")
  if(arg_SUBDIR)
    set(subdir "${arg_SUBDIR}")
  endif()
  set(entries)
  foreach(file IN LISTS arg_UNPARSED_ARGUMENTS)
    cmake_path(ABSOLUTE_PATH file NORMALIZE)
    list(APPEND entries "${subdir}|${file}")
  endforeach()
  get_property(type TARGET ${target} PROPERTY TYPE)
  if(type MATCHES "^(EXECUTABLE|SHARED_LIBRARY|MODULE_LIBRARY)$")
    set_property(TARGET ${target} APPEND PROPERTY DAGOR_RUNTIME_FILES ${entries})
  else()
    set_property(TARGET ${target} APPEND PROPERTY INTERFACE_DAGOR_RUNTIME_FILES ${entries})
  endif()
endfunction()

# the runtime files and the license of a program: lists of what its link closure has (custom transitive properties),
# made into files per configuration, which a step after its link copies or concatenates next to it
function(_dagor_program_files target)
  set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}")
  file(GENERATE OUTPUT "${gen}/runtime-$<CONFIG>.txt"
    CONTENT "$<JOIN:$<REMOVE_DUPLICATES:$<TARGET_PROPERTY:${target},DAGOR_RUNTIME_FILES>>,\n>\n" TARGET ${target})
  file(GENERATE OUTPUT "${gen}/licenses-$<CONFIG>.txt"
    CONTENT "$<JOIN:$<REMOVE_DUPLICATES:$<TARGET_PROPERTY:${target},DAGOR_LICENSE_FILES>>,\n>\n" TARGET ${target})
  # an app bundle's license goes to its Resources, its MacOS dir holds code only
  set(license_dir "$<TARGET_FILE_DIR:${target}>$<$<BOOL:$<TARGET_PROPERTY:${target},MACOSX_BUNDLE>>:/../Resources>")
  add_custom_command(TARGET ${target} POST_BUILD
    COMMAND "${CMAKE_COMMAND}" -DLIST=${gen}/runtime-$<CONFIG>.txt -DDEST=$<TARGET_FILE_DIR:${target}>
      -P "${DAGOR_CMAKE_DIR}/scripts/copy_runtime_files.cmake"
    COMMAND "${CMAKE_COMMAND}" -DLIST=${gen}/licenses-$<CONFIG>.txt -DPROGRAM=$<TARGET_FILE_NAME:${target}>
      "-DOUT=${license_dir}/LICENSE-$<TARGET_FILE_BASE_NAME:${target}>" -P "${DAGOR_CMAKE_DIR}/scripts/write_license.cmake"
    VERBATIM)
  set_property(TARGET ${target} PROPERTY DAGOR_PROGRAM_FILES_DIR "${gen}")
endfunction()

# dagor_install_program(<target> DESTINATION <dir> COMPONENT <component>): installs a program or shared library with its
# runtime files, its LICENSE file and (MSVC) its debug info
function(dagor_install_program target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "DESTINATION;COMPONENT" "")
  install(TARGETS ${target}
    RUNTIME DESTINATION "${arg_DESTINATION}" COMPONENT ${arg_COMPONENT}
    LIBRARY DESTINATION "${arg_DESTINATION}" COMPONENT ${arg_COMPONENT}
    BUNDLE DESTINATION "${arg_DESTINATION}" COMPONENT ${arg_COMPONENT})
  if(MSVC)
    install(FILES "$<TARGET_PDB_FILE:${target}>" DESTINATION "${arg_DESTINATION}" COMPONENT ${arg_COMPONENT} OPTIONAL)
  endif()
  get_property(gen TARGET ${target} PROPERTY DAGOR_PROGRAM_FILES_DIR)
  # next to the program; in an app bundle, the runtime files next to it in Contents/MacOS, the license in Resources
  set(dest "${arg_DESTINATION}")
  set(license_dest "${arg_DESTINATION}")
  set(license_dir "$<TARGET_FILE_DIR:${target}>")
  get_property(bundle TARGET ${target} PROPERTY MACOSX_BUNDLE)
  if(bundle)
    set(dest "${arg_DESTINATION}/$<TARGET_FILE_NAME:${target}>.app/Contents/MacOS")
    set(license_dest "${arg_DESTINATION}/$<TARGET_FILE_NAME:${target}>.app/Contents/Resources")
    set(license_dir "$<TARGET_FILE_DIR:${target}>/../Resources")
  endif()
  install(CODE "set(_prefix \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}\")
execute_process(COMMAND \"${CMAKE_COMMAND}\" \"-DLIST=${gen}/runtime-$<CONFIG>.txt\" \"-DDEST=\${_prefix}/${dest}\"
  -P \"${DAGOR_CMAKE_DIR}/scripts/copy_runtime_files.cmake\" COMMAND_ERROR_IS_FATAL ANY)
if(EXISTS \"${license_dir}/LICENSE-$<TARGET_FILE_BASE_NAME:${target}>\")
  file(INSTALL \"${license_dir}/LICENSE-$<TARGET_FILE_BASE_NAME:${target}>\" DESTINATION \"\${_prefix}/${license_dest}\")
endif()"
    COMPONENT ${arg_COMPONENT})
endfunction()

# dagor_target_force_include(<target> <header>...): the C and C++ sources of <target> start with the headers (a
# header of the calling dir by its path: the compilers search their working dir, not the source's)
function(dagor_target_force_include target)
  foreach(header IN LISTS ARGN)
    if(NOT IS_ABSOLUTE "${header}" AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${header}")
      set(header "${CMAKE_CURRENT_SOURCE_DIR}/${header}")
    endif()
    if(MSVC)
      target_compile_options(${target} PRIVATE "$<$<COMPILE_LANGUAGE:C,CXX>:/FI${header}>")
    else()
      target_compile_options(${target} PRIVATE "$<$<COMPILE_LANGUAGE:C,CXX,OBJCXX>:SHELL:-include ${header}>")
    endif()
  endforeach()
endfunction()

# dagor_glob_sources(<out-var> DIRS <dir>... [GLOB <pattern>...] [EXCLUDE <regex>...]): appends to <out-var> the files
# of the dirs (relative to the calling dir, not recursive) that match the patterns (default *.cpp *.c), sorted;
# *.gen.es.cpp files are made by the ES codegen and never listed. jam's AutoscanBuildLists.
function(dagor_glob_sources out)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "" "DIRS;GLOB;EXCLUDE")
  if(NOT arg_GLOB)
    set(arg_GLOB *.cpp *.c)
  endif()
  set(result ${${out}})
  foreach(dir IN LISTS arg_DIRS)
    cmake_path(ABSOLUTE_PATH dir NORMALIZE)
    set(patterns ${arg_GLOB})
    list(TRANSFORM patterns PREPEND "${dir}/")
    file(GLOB found CONFIGURE_DEPENDS ${patterns})
    list(FILTER found EXCLUDE REGEX "\\.gen\\.es\\.cpp$")
    foreach(regex IN LISTS arg_EXCLUDE)
      list(FILTER found EXCLUDE REGEX "${regex}")
    endforeach()
    list(SORT found)
    list(APPEND result ${found})
  endforeach()
  set(${out} "${result}" PARENT_SCOPE)
endfunction()

# dagor_add_link_choice(<name> PROPERTY <property> ON <target> OFF <target>): an interface library that links <ON>
# into the programs whose <property> is true and <OFF> into the others. A program sets the property, or gets it from a
# library it links that sets INTERFACE_<property> ON. This is how a choice jam made with a global variable is made per
# program when libraries in between depend on the chosen one; both implementations are built only for the programs
# that use them.
function(dagor_add_link_choice name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "PROPERTY;ON;OFF" "")
  add_library(${name} INTERFACE)
  target_link_libraries(${name} INTERFACE "$<IF:$<BOOL:$<TARGET_PROPERTY:${arg_PROPERTY}>>,${arg_ON},${arg_OFF}>")
  set_property(TARGET ${name} APPEND PROPERTY COMPATIBLE_INTERFACE_BOOL ${arg_PROPERTY})
endfunction()

# dagor_add_link_select(<name> PROPERTY <property> DEFAULT <target> [<value> <target>]...): like dagor_add_link_choice,
# for a string property: the programs whose <property> is <value> get that <target>, the others (and those without
# the property) get the DEFAULT one
function(dagor_add_link_select name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "PROPERTY;DEFAULT" "")
  set(pairs ${arg_UNPARSED_ARGUMENTS})
  set(expr "${arg_DEFAULT}")
  set(property "$<TARGET_PROPERTY:${arg_PROPERTY}>")
  while(pairs)
    list(POP_BACK pairs target value)
    set(expr "$<IF:$<STREQUAL:${property},${value}>,${target},${expr}>")
  endwhile()
  add_library(${name} INTERFACE)
  target_link_libraries(${name} INTERFACE "${expr}")
  set_property(TARGET ${name} APPEND PROPERTY COMPATIBLE_INTERFACE_STRING ${arg_PROPERTY})
endfunction()

# the object library with dagor_exe_build_date/_time (dagor_get_build_stamp_str), linked into every program
block()
  if(DAGOR_BUILD_STAMP)
    string(TIMESTAMP date "%b %d %Y")
    string(TIMESTAMP time "%H:%M:%S")
  else()
    set(date "*")
    set(time "*")
  endif()
  file(CONFIGURE OUTPUT "${CMAKE_BINARY_DIR}/dagor/buildStamp.c" CONTENT
    "const char *dagor_exe_build_date = \"${date}\";\nconst char *dagor_exe_build_time = \"${time}\";\n")
  add_library(dagor.buildStamp OBJECT "${CMAKE_BINARY_DIR}/dagor/buildStamp.c")
  set_property(TARGET dagor.buildStamp PROPERTY FOLDER "dagor")
endblock()
