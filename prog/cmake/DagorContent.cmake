# Content built by the tree's tools: dagor_add_shaders() (tracked by CMake), dagor_add_content_step() (tracked by its
# tool).
#
# dagor_add_shaders(<name> COMPILER <dsc2 tool> BLK <shaders.blk> OUTPUT <dir>/<base> [ARGS <compiler args>...]
#                   [INSTALL <dir> COMPONENT <component>])
# A target that compiles the shaders of <shaders.blk> with a shader compiler (dsc2-dx12, ...: dagor_host_tool) into the
# dumps <dir>/<base>.<profile>.shdump.bin, when the compiler or a shader source changes (the .dshl/.hlsl files of the
# blk's dir and of its incDir dirs). It runs in the blk's dir (the base of its relative paths); the intermediate files go to
# the build dir. INSTALL also installs the dumps into <dir> of the install prefix (when the tree made them). Not in the
# default build: the tree that ships the shaders adds it (dagor_build_by_default).
include_guard(GLOBAL)

# The content tools already parallelize internally (shader compilers fork one
# worker per CPU). Keep Ninja from launching several such tools at once.
set_property(GLOBAL APPEND PROPERTY JOB_POOLS dagor_content=1)

function(dagor_add_shaders name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "COMPILER;BLK;OUTPUT;INSTALL;COMPONENT" "ARGS")
  foreach(required COMPILER BLK OUTPUT)
    if(NOT arg_${required})
      message(FATAL_ERROR "dagor_add_shaders(${name}): ${required} is required")
    endif()
  endforeach()
  cmake_path(ABSOLUTE_PATH arg_BLK NORMALIZE OUTPUT_VARIABLE blk)
  cmake_path(GET blk PARENT_PATH blk_dir)
  cmake_path(GET arg_OUTPUT PARENT_PATH out_dir)
  cmake_path(GET arg_OUTPUT FILENAME out_base)

  # the shader sources: the blks of the blk's dir, the blk's dir and the incDir:t="..." dirs of the blk and of the blks
  # it includes (include <file>)
  set(blks "${blk}")
  file(STRINGS "${blk}" include_lines REGEX "^[ \t]*include[ \t]")
  foreach(line IN LISTS include_lines)
    if(line MATCHES "^[ \t]*include[ \t]+\"?([^\" \t]+)")
      cmake_path(ABSOLUTE_PATH CMAKE_MATCH_1 BASE_DIRECTORY "${blk_dir}" NORMALIZE OUTPUT_VARIABLE included)
      if(EXISTS "${included}")
        list(APPEND blks "${included}")
      endif()
    endif()
  endforeach()
  set(dirs "${blk_dir}")
  foreach(file IN LISTS blks)
    file(STRINGS "${file}" inc_lines REGEX "^[ \t]*incDir:t[ \t]*=")
    foreach(line IN LISTS inc_lines)
      if(line MATCHES "\"([^\"]+)\"")
        cmake_path(ABSOLUTE_PATH CMAKE_MATCH_1 BASE_DIRECTORY "${blk_dir}" NORMALIZE OUTPUT_VARIABLE dir)
        list(APPEND dirs "${dir}")
      endif()
    endforeach()
  endforeach()
  list(REMOVE_DUPLICATES dirs)
  set(patterns "${blk_dir}/*.blk")
  foreach(dir IN LISTS dirs)
    list(APPEND patterns "${dir}/*.dshl" "${dir}/*.hlsl" "${dir}/*.hlsli" "${dir}/*.sh")
  endforeach()
  file(GLOB_RECURSE shader_sources CONFIGURE_DEPENDS ${patterns})

  dagor_host_tool(${arg_COMPILER} compiler)
  set(work "${CMAKE_CURRENT_BINARY_DIR}/shaders/${name}")
  set(stamp "${work}/${name}.stamp")
  add_custom_command(OUTPUT "${stamp}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${out_dir}"
    COMMAND "${compiler}" "${blk}" -out "${arg_OUTPUT}" -q -shaderOn -nodisassembly -commentPP
      -codeDumpErr ${arg_ARGS} -o "${work}/obj"
    COMMAND "${CMAKE_COMMAND}" -E touch "${stamp}"
    WORKING_DIRECTORY "${blk_dir}"
    DEPENDS "${blk}" ${shader_sources} ${compiler_DEPENDS}
    COMMENT "Compiling the shaders of ${name} (${arg_COMPILER})"
    JOB_POOL dagor_content
    VERBATIM)
  add_custom_target(${name} DEPENDS "${stamp}") # in the default build of the tree that ships it (dagor_build_by_default)
  set_property(TARGET ${name} PROPERTY FOLDER "shaders")
  if(arg_INSTALL)
    if(NOT arg_COMPONENT)
      message(FATAL_ERROR "dagor_add_shaders(${name}): INSTALL needs a COMPONENT")
    endif()
    install(DIRECTORY "${out_dir}/" DESTINATION "${arg_INSTALL}" COMPONENT "${arg_COMPONENT}" OPTIONAL
      FILES_MATCHING PATTERN "${out_base}.*.shdump.bin")
  endif()
endfunction()

# dagor_add_content_step(<name> (TOOL <engine tool> | COMMAND <command>...) [ARGS <argument>...]
#                        [WORKING_DIRECTORY <dir>] [GROUP <target>] [DEPENDS <target>...] [COMMENT <text>])
# A target that runs an engine tool (dagor_host_tool) or a command whenever it is built, for content whose tool keeps track of what changed itself (the shader compilers'
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
    cmake_path(ABSOLUTE_PATH arg_WORKING_DIRECTORY NORMALIZE OUTPUT_VARIABLE dir)
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
    JOB_POOL dagor_content
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
