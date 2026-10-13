# daScript compiled ahead of time (DAGOR_DAS_AOT, game trees):
#
#   dagor_target_das_aot(<target> PULL <variable> <file>.das...)
#
# translates the files to C++ with the game's AOT compiler and compiles them into <target>, in batches of
# DAGOR_DAS_AOT_BATCH. Each batch defines aot_<batch>_pull; <variable> references
# them all (in a program: is just defined), and the code that pulls the target's daScript in names it (e.g.
# ecs_aot_DAS_pull_AOT of gameLibs/das/ecs). Without DAGOR_DAS_AOT <variable> is 0, for the code that names it anyway
# (the game's pull of its modules).
#
# The AOT compiler is a host program of the game (daNetGame-das-aot with the game's daScript modules), which
# dagor_add_dng_game() sets up as target dagor.dasAotCompiler: the project's <host>-aot-compiler preset
# (DAGOR_DAS_AOT_COMPILER), configured once and built in Dev, under a lock, for all of the project's trees; it runs in
# the game's prog dir (its aot_config.blk). DAGOR_DAS_AOT_COMPILER_PATH names a prebuilt one instead. The libraries
# with daScript are configured before the game is declared, so they name the compiler through the target's properties.
include_guard(GLOBAL)

set(DAGOR_DAS_AOT_COMPILER_PATH "" CACHE FILEPATH "A prebuilt daScript AOT compiler of the game; empty builds it")
set(DAGOR_DAS_AOT_BATCH 10 CACHE STRING "daScript files per AOT-compiled C++ batch")

# _dagor_das_aot_compiler(<game> <prog dir>): target dagor.dasAotCompiler, for dagor_add_dng_game()
function(_dagor_das_aot_compiler game prog_dir)
  string(TOLOWER "${DAGOR_HOST_PLATFORM}" host)
  set(preset ${host}-aot-compiler)
  set(exe "${DAGOR_DAS_AOT_COMPILER_PATH}")
  set(commands)
  if(NOT exe)
    cmake_path(GET prog_dir PARENT_PATH root)
    set(exe "${root}/build/${preset}/bin/${game}-aot-dev${CMAKE_HOST_EXECUTABLE_SUFFIX}")
    set(commands COMMAND "${CMAKE_COMMAND}" -E env DAGOR_DEPS_DIR=${DAGOR_DEPS_DIR}
      "${CMAKE_COMMAND}" -DSOURCE_DIR=${prog_dir} -DPRESET=${preset} -DTARGETS=${game}-aot
      -P "${DAGOR_CMAKE_DIR}/scripts/build_preset.cmake")
  endif()
  add_custom_target(dagor.dasAotCompiler ${commands}
    BYPRODUCTS "${exe}"
    COMMENT "daScript AOT compiler of ${game} (${preset}, Dev)"
    USES_TERMINAL
    VERBATIM)
  set_target_properties(dagor.dasAotCompiler PROPERTIES FOLDER "dagor" DAGOR_EXECUTABLE "${exe}"
    DAGOR_WORKING_DIRECTORY "${prog_dir}")
endfunction()

function(dagor_target_das_aot target)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "PULL" "")
  if(NOT arg_PULL)
    message(FATAL_ERROR "dagor_target_das_aot(${target}): PULL <variable> is required")
  endif()
  set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}/das")
  if(NOT DAGOR_DAS_AOT)
    file(CONFIGURE OUTPUT "${gen}/pull.cpp" CONTENT "#include <stddef.h>
size_t ${arg_PULL} = 0;
")
    target_sources(${target} PRIVATE "${gen}/pull.cpp")
    return()
  endif()
  get_target_property(type ${target} TYPE)
  set(compiler "$<TARGET_PROPERTY:dagor.dasAotCompiler,DAGOR_EXECUTABLE>")
  set(files)
  foreach(file IN LISTS arg_UNPARSED_ARGUMENTS)
    if(file MATCHES "^\\$<") # a file of some configurations only (a generator expression): it runs interpreted
      continue()
    endif()
    cmake_path(ABSOLUTE_PATH file NORMALIZE)
    list(APPEND files "${file}")
  endforeach()

  set(batch_index 0)
  set(anchors)
  set(aot_outputs)
  while(files)
    list(LENGTH files count)
    set(n ${count})
    if(n GREATER DAGOR_DAS_AOT_BATCH)
      set(n ${DAGOR_DAS_AOT_BATCH})
    endif()
    list(SUBLIST files 0 ${n} batch)
    if(n LESS count)
      list(SUBLIST files ${n} -1 files)
    else()
      set(files)
    endif()

    set(args)
    set(outputs)
    set(text "#include <stddef.h>\n")
    foreach(src IN LISTS batch)
      cmake_path(RELATIVE_PATH src BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}" OUTPUT_VARIABLE rel)
      string(REGEX REPLACE "\\.das$" "_das_AOT.cpp" rel "${rel}")
      string(REPLACE "../" "__/" rel "${rel}")
      list(APPEND args -aot "${src}" "${gen}/$<CONFIG>/${rel}")
      list(APPEND outputs "${gen}/$<CONFIG>/${rel}")
      string(APPEND text "#include \"${gen}/$<CONFIG>/${rel}\"\n")
    endforeach()
    string(MAKE_C_IDENTIFIER "das_batch_${target}_${batch_index}" anchor)
    string(APPEND text "size_t aot_${anchor}_pull = (size_t)&aot_${anchor}_pull;\n")
    list(APPEND anchors "aot_${anchor}_pull")
    add_custom_command(OUTPUT ${outputs}
      COMMAND "${compiler}" "${DAGOR_PROG_DIR}/1stPartyLibs/daScript/utils/aot/main.das"
        -- --config aot_config.blk -sConfig "$<LOWER_CASE:$<CONFIG>>"
        -force-overwrite -gen1 true -gen2-make true ${args}
      DEPENDS ${batch} dagor.dasAotCompiler "${compiler}"
      WORKING_DIRECTORY "$<TARGET_PROPERTY:dagor.dasAotCompiler,DAGOR_WORKING_DIRECTORY>"
      COMMENT "daScript AOT: ${anchor}"
      VERBATIM)
    list(APPEND aot_outputs ${outputs})
    file(GENERATE OUTPUT "${gen}/$<CONFIG>/batch${batch_index}.cpp" CONTENT "${text}")
    target_sources(${target} PRIVATE "${gen}/$<CONFIG>/batch${batch_index}.cpp")
    math(EXPR batch_index "${batch_index} + 1")
  endwhile()

  # the target's pull: a library keeps only the objects something references, a program has them all
  if(NOT anchors OR type MATCHES "^(EXECUTABLE|SHARED_LIBRARY)$")
    set(text "#include <stddef.h>\nsize_t ${arg_PULL} = 0;\n")
  else()
    list(JOIN anchors ", " externs)
    list(JOIN anchors " + " sum)
    set(text "#include <stddef.h>\nextern size_t ${externs};\nsize_t ${arg_PULL} = 0 + ${sum};\n")
  endif()
  file(CONFIGURE OUTPUT "${gen}/pull.cpp" CONTENT "${text}")
  target_sources(${target} PRIVATE "${gen}/pull.cpp")
  # the batches include the translated scripts (their dependency files then track them): made before the target compiles
  if(aot_outputs)
    add_custom_target(${target}.dasAot DEPENDS ${aot_outputs})
    set_property(TARGET ${target}.dasAot PROPERTY FOLDER "dagor")
    add_dependencies(${target} ${target}.dasAot)
  endif()
  # what the translated scripts include
  target_include_directories(${target} PRIVATE ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
    ${DAGOR_PROG_DIR}/gameLibs/publicInclude)
endfunction()
