# Content built by the tree's tools: dagor_add_shaders() (tracked by CMake), dagor_add_content_step() (tracked by its
# tool).
#
# dagor_add_shaders(<name> COMPILER <dsc2 target> BLK <shaders.blk> OUTPUT <dir>/<base> [ARGS <compiler args>...]
#                   [INSTALL <dir> COMPONENT <component>])
# A target that compiles the shaders of <shaders.blk> with a shader compiler of the tree (dsc2-dx12, ...) into the
# dumps <dir>/<base>.<profile>.shdump.bin, when the compiler or a shader source changes (the .dshl/.hlsl files of the
# blk's dir and of its incDir dirs). It runs in the blk's dir, as the shader scripts did; the intermediate files go to
# the build dir. INSTALL also installs the dumps into <dir> of the install prefix.
include_guard(GLOBAL)

function(dagor_add_shaders name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "COMPILER;BLK;OUTPUT;INSTALL;COMPONENT" "ARGS")
  foreach(required COMPILER BLK OUTPUT)
    if(NOT arg_${required})
      message(FATAL_ERROR "dagor_add_shaders(${name}): ${required} is required")
    endif()
  endforeach()
  _dagor_abs_paths(blk "${arg_BLK}")
  cmake_path(GET blk PARENT_PATH blk_dir)
  cmake_path(GET arg_OUTPUT PARENT_PATH out_dir)
  cmake_path(GET arg_OUTPUT FILENAME out_base)

  # the shader sources: the blk's dir and its incDir:t="..." dirs
  set(dirs "${blk_dir}")
  file(STRINGS "${blk}" inc_lines REGEX "^[ \t]*incDir:t[ \t]*=")
  foreach(line IN LISTS inc_lines)
    if(line MATCHES "\"([^\"]+)\"")
      cmake_path(ABSOLUTE_PATH CMAKE_MATCH_1 BASE_DIRECTORY "${blk_dir}" NORMALIZE OUTPUT_VARIABLE dir)
      list(APPEND dirs "${dir}")
    endif()
  endforeach()
  set(patterns)
  foreach(dir IN LISTS dirs)
    list(APPEND patterns "${dir}/*.dshl" "${dir}/*.hlsl" "${dir}/*.hlsli" "${dir}/*.sh")
  endforeach()
  file(GLOB_RECURSE shader_sources CONFIGURE_DEPENDS ${patterns})

  set(work "${CMAKE_CURRENT_BINARY_DIR}/shaders/${name}")
  set(stamp "${work}/${name}.stamp")
  add_custom_command(OUTPUT "${stamp}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${out_dir}"
    COMMAND "$<TARGET_FILE:${arg_COMPILER}>" "${blk}" -out "${arg_OUTPUT}" -q -shaderOn -nodisassembly -commentPP
      -codeDumpErr ${arg_ARGS} -o "${work}/obj"
    COMMAND "${CMAKE_COMMAND}" -E touch "${stamp}"
    WORKING_DIRECTORY "${blk_dir}"
    DEPENDS "${blk}" ${shader_sources} ${arg_COMPILER}
    COMMENT "Compiling the shaders of ${name} (${arg_COMPILER})"
    VERBATIM)
  add_custom_target(${name} ALL DEPENDS "${stamp}")
  set_property(TARGET ${name} PROPERTY FOLDER "shaders")
  if(arg_INSTALL)
    if(NOT arg_COMPONENT)
      message(FATAL_ERROR "dagor_add_shaders(${name}): INSTALL needs a COMPONENT")
    endif()
    install(DIRECTORY "${out_dir}/" DESTINATION "${arg_INSTALL}" COMPONENT "${arg_COMPONENT}"
      FILES_MATCHING PATTERN "${out_base}.*.shdump.bin")
  endif()
endfunction()

# dagor_add_content_step(<name> (TOOL <engine tool> | COMMAND <command>...) [ARGS <argument>...]
#                        [WORKING_DIRECTORY <dir>] [GROUP <target>] [DEPENDS <target>...] [COMMENT <text>])
# A target that runs an engine tool (dagor_host_tool: the tree's own, a CDK's or the host CDK built on demand) or a
# command whenever it is built, for content whose tool keeps track of what changed itself (the shader compilers'
# caches, daBuild's, vromfsPacker): a game's shaders, vromfs and assets. It is not part of the default build; GROUP
# (a target made on first use) builds it with the other steps of that group, DEPENDS after other steps.
function(dagor_add_content_step name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "TOOL;WORKING_DIRECTORY;GROUP;COMMENT" "COMMAND;ARGS;DEPENDS")
  if(arg_UNPARSED_ARGUMENTS OR (NOT arg_TOOL AND NOT arg_COMMAND) OR (arg_TOOL AND arg_COMMAND))
    message(FATAL_ERROR "dagor_add_content_step(${name} TOOL <tool> | COMMAND <command>... ...)")
  endif()
  set(tool_DEPENDS)
  if(arg_TOOL)
    dagor_host_tool(${arg_TOOL} tool)
    set(command "${tool}")
  else()
    set(command ${arg_COMMAND})
  endif()
  set(dir "${CMAKE_CURRENT_SOURCE_DIR}")
  if(arg_WORKING_DIRECTORY)
    _dagor_abs_paths(dir "${arg_WORKING_DIRECTORY}")
  endif()
  set(comment "${arg_COMMENT}")
  if(NOT comment)
    set(comment "${name}")
  endif()
  # a symbolic output: never made, so the step runs every time its target is built
  set(run "${CMAKE_CURRENT_BINARY_DIR}/content/${name}.run")
  set_source_files_properties("${run}" PROPERTIES SYMBOLIC ON)
  add_custom_command(OUTPUT "${run}"
    COMMAND ${command} ${arg_ARGS}
    WORKING_DIRECTORY "${dir}"
    DEPENDS ${tool_DEPENDS}
    COMMENT "${comment}"
    VERBATIM)
  add_custom_target(${name} DEPENDS "${run}")
  set_property(TARGET ${name} PROPERTY FOLDER "content")
  if(arg_DEPENDS)
    add_dependencies(${name} ${arg_DEPENDS})
  endif()
  if(arg_GROUP)
    if(NOT TARGET ${arg_GROUP})
      add_custom_target(${arg_GROUP})
      set_property(TARGET ${arg_GROUP} PROPERTY FOLDER "content")
    endif()
    add_dependencies(${arg_GROUP} ${name})
  endif()
endfunction()
