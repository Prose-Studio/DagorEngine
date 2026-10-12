# Games on daNetGame (DAGOR_VARIANT game: the trees of projects, e.g. templates/dng-empty): the game's switches, its
# modules (daNetGameLibs, and gameLibs built like them) and the game program.
include_guard(GLOBAL)

# --- the game's switches (prog/daNetGame/setup.jam) -------------------------------------------------------------------
# DAGOR_GAME_<X> is ON or OFF for the whole tree. Those jam left out of Rel builds only are generator expressions that
# are true in the other configurations, for $<IF:...> and $<...:...> (DAGOR_GAME_DEV: not Rel):
#   DAGOR_GAME_EDITOR (embedded daEditorE), DAGOR_GAME_WEBUI, DAGOR_GAME_CONSOLE, DAGOR_GAME_IMGUI
set(DAGOR_GAME_DEV "$<NOT:$<CONFIG:Rel>>")
set(DAGOR_GAME_RENDERER ON)
if(DAGOR_DEDICATED)
  set(DAGOR_GAME_RENDERER OFF) # headless
endif()
set(DAGOR_GAME_FX ${DAGOR_GAME_RENDERER})
set(DAGOR_GAME_OVERLAY_UI ${DAGOR_GAME_RENDERER})
set(DAGOR_GAME_DNG_INPUT ${DAGOR_GAME_RENDERER})
set(DAGOR_GAME_CONTENT_UPDATER ${DAGOR_GAME_RENDERER})
set(DAGOR_GAME_SOUND_NET ON)
option(DAGOR_GAME_THREAD_SAFE_NET_TIME "Guard daNetGame's net time manager with a lock (sync time readable from any thread)"
  OFF)
# sound needs FMOD, which is not redistributable
option(DAGOR_GAME_SOUND "The game client's sound (FMOD Studio)" OFF)
if(DAGOR_DEDICATED)
  set(DAGOR_GAME_SOUND OFF)
endif()
set(DAGOR_GAME_EMBEDDED_BROWSER OFF)
set(DAGOR_GAME_ASSET_MANAGER OFF)
# BVH ray tracing: on the platforms and CPUs that have it
set(DAGOR_GAME_BVH OFF)
if(DAGOR_GAME_RENDERER AND ((WIN32 AND DAGOR_ARCH STREQUAL "x86_64" AND DAGOR_SSE EQUAL 4) OR LINUX))
  set(DAGOR_GAME_BVH ON)
endif()
set(DAGOR_BVH_STUBS grass) # without the random grass (prog/gameLibs/bvh/CMakeLists.txt)
# the render graph with its daScript bindings and its daECS nodes (prog/gameLibs/render/daFrameGraph)
if(DAGOR_VARIANT STREQUAL "game")
  set(DAGOR_DAFG_FEATURES das ecs)
endif()
# the developer features outside Rel
set(_desktop OFF)
if(CMAKE_SYSTEM_NAME MATCHES "^(Windows|Linux|Darwin)$")
  set(_desktop ON)
endif()
set(DAGOR_GAME_EDITOR 0)
if(DAGOR_GAME_RENDERER AND _desktop)
  set(DAGOR_GAME_EDITOR "${DAGOR_GAME_DEV}")
endif()
set(DAGOR_GAME_WEBUI "${DAGOR_GAME_DEV}")
if(DAGOR_DEDICATED AND LINUX)
  set(DAGOR_GAME_WEBUI 0)
endif()
set(DAGOR_GAME_CONSOLE "${DAGOR_GAME_DEV}")
if(WIN32 AND DAGOR_ARCH STREQUAL "x86_64")
  set(DAGOR_GAME_CONSOLE 1)
endif()
set(DAGOR_GAME_IMGUI 0)
if(DAGOR_GAME_RENDERER)
  set(DAGOR_GAME_IMGUI "${DAGOR_GAME_DEV}")
endif()
unset(_desktop)

# the include dirs of daNetGame and the game programs (prog/daNetGame/setup.jam), and their options: clang's unused
# variables are errors there
set(DAGOR_DNG_INCLUDES
  ${DAGOR_PROG_DIR}/daNetGame
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude
  ${DAGOR_PROG_DIR}/gameLibs/publicInclude/quirrel
  ${DAGOR_PROG_DIR}/gameLibs/render/screenSpaceReflection
  ${DAGOR_PROG_DIR}/commonFx/commonFxGame
  ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/Detour/Include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/recastnavigation/DetourTileCache/Include
  ${DAGOR_PROG_DIR}/1stPartyLibs/jsoncpp/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/rapidJsonUtils/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zlib-ng
  ${DAGOR_PROG_DIR}/3rdPartyLibs/arc/zstd-1.4.5 # xxhash
  ${DAGOR_PROG_DIR}/3rdPartyLibs/libb64/include
  ${DAGOR_PROG_DIR}/3rdPartyLibs/rapidjson/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/include
  ${DAGOR_PROG_DIR}/1stPartyLibs/daScript/modules/dasQuirrel/src
)
set(DAGOR_DNG_OPTIONS "$<$<CXX_COMPILER_ID:Clang,AppleClang>:-Werror=unused-variable>")

# --- generated sources ------------------------------------------------------------------------------------------------
# _dagor_generate_source(<target> <file> <content>): adds the generated source to <target>; content with generator
# expressions is written per configuration (<file> with -<config> before its extension)
function(_dagor_generate_source target file content)
  if(content MATCHES "\\$<")
    cmake_path(REMOVE_EXTENSION file LAST_ONLY OUTPUT_VARIABLE stem)
    cmake_path(GET file EXTENSION LAST_ONLY ext)
    file(GENERATE OUTPUT "${stem}-$<CONFIG>${ext}" CONTENT "${content}" TARGET ${target})
    target_sources(${target} PRIVATE "${stem}-$<CONFIG>${ext}")
  else()
    file(CONFIGURE OUTPUT "${file}" CONTENT "${content}")
    target_sources(${target} PRIVATE "${file}")
  endif()
endfunction()

# _dagor_pull_file(<target> <file> ECS|EXTERN <variable> <pull>...): adds to <target> the source that defines size_t
# <variable>, the sum of the pulls, which makes the linker keep the objects that define them: ECS_PULL_VAR(<pull>) of
# entity systems or plain extern size_t variables. A pull $<cond:name> is there in the configurations where cond holds.
function(_dagor_pull_file target file kind variable)
  set(bs "\\")
  set(text "#include <daECS/core/componentType.h>\n#define REG_SYS${bs}\n")
  foreach(pull IN LISTS ARGN)
    if(pull MATCHES "^\\$<(.+):([A-Za-z_][A-Za-z0-9_]*)>$")
      string(APPEND text "$<${CMAKE_MATCH_1}:  RS(${CMAKE_MATCH_2})${bs}\n>")
    else()
      string(APPEND text "  RS(${pull})${bs}\n")
    endif()
  endforeach()
  if(kind STREQUAL "ECS")
    string(APPEND text "\n#define RS(x) ECS_DECL_PULL_VAR(x);\nREG_SYS\n#undef RS\n#define RS(x) + ECS_PULL_VAR(x)\n")
  else()
    string(APPEND text "\n#define RS(x) extern size_t x;\nREG_SYS\n#undef RS\n#define RS(x) + (x)\n")
  endif()
  string(APPEND text "size_t ${variable} = 0 REG_SYS;\n")
  _dagor_generate_source(${target} "${file}" "${text}")
endfunction()

# --- modules (prog/_jBuild/build_module.jam) --------------------------------------------------------------------------
# dagor_add_dng_module(NAME <target> <dagor_add_target arguments> [DAS] [PULL_VARS <name>...])
# A game module (daNetGameLibs/<module>, or a gameLibs dir built like one): a strict static library with the pull file
# that references its entity systems (ES_FILES) and PULL_VARS as framework_<module>_pull (<module> is the directory's
# name). A DAS module's daScript (DAS_FILES) is pulled by <area>_<module>_DAS_pull_AOT.
function(dagor_add_dng_module)
  cmake_parse_arguments(PARSE_ARGV 0 arg "${_DAGOR_TARGET_OPTIONS};DAS" "${_DAGOR_TARGET_ONE_VALUE}"
                        "${_DAGOR_TARGET_MULTI_VALUE};PULL_VARS")
  set(target ${arg_NAME})
  cmake_path(GET CMAKE_CURRENT_SOURCE_DIR FILENAME module)
  cmake_path(RELATIVE_PATH CMAKE_CURRENT_SOURCE_DIR BASE_DIRECTORY "${DAGOR_PROG_DIR}" OUTPUT_VARIABLE rel)
  string(REGEX MATCH "^[^/]+" area "${rel}")
  if(arg_DAS)
    string(MAKE_C_IDENTIFIER "${area}-${module}_DAS_pull_AOT" arg_DAS_PULL)
  endif()
  _dagor_target_arguments(args)
  dagor_add_target(${args})
  target_link_libraries(${target} PRIVATE Dagor::Quirrel)
  target_compile_definitions(${target} PRIVATE DISABLE_SYNC_DEBUG) # the fork has no gameLibs/syncDebug

  _dagor_es_pulls(${target} pulls)
  _dagor_pull_file(${target} "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}/${module}_es_pull.cpp" ECS
    "framework_${module}_pull" ${arg_PULL_VARS} ${pulls})
endfunction()

# _dagor_es_pulls(<target> <out-var>): the pulls of the entity systems of <target> (dagor_target_es_sources), named
# after their files (<name>ES.cpp.inl); $<cond:name> for those built where cond holds
function(_dagor_es_pulls target out)
  get_property(entries TARGET ${target} PROPERTY DAGOR_ES_FILES)
  set(pulls)
  foreach(entry IN LISTS entries)
    string(REGEX MATCH "^[^|]*" cond "${entry}")
    string(REGEX REPLACE "^[^|]*\\|" "" path "${entry}")
    cmake_path(GET path FILENAME name)
    string(REGEX REPLACE "ES\\.cpp\\.inl$" "" name "${name}")
    if(cond)
      list(APPEND pulls "$<${cond}:${name}>")
    else()
      list(APPEND pulls "${name}")
    endif()
  endforeach()
  set(${out} ${pulls} PARENT_SCOPE)
endfunction()

# --- what a library adds to the game program (the libraries' _lib.cmake) ----------------------------------------------
# dagor_game_lib([PULLS <pull>...] [INCLUDES <dir>...] [LINK <target>...] [SOURCES <file>...]): the game program of the
# tree (its AOT compiler in a DAGOR_DAS_AOT_COMPILER tree) references the pulls, compiles with the include dirs and the
# sources (relative to the calling file's dir), and links the libraries. A library's own CMakeLists.txt, which comes
# before the game, names the pulls the game needs when it links the library in INTERFACE_DAGOR_GAME_PULLS (a custom
# transitive property: the game gets those of its whole link closure).
function(dagor_game_lib)
  cmake_parse_arguments(PARSE_ARGV 0 arg "" "" "PULLS;INCLUDES;LINK;SOURCES")
  get_property(game GLOBAL PROPERTY DAGOR_GAME_TARGET)
  if(NOT game)
    message(FATAL_ERROR "dagor_game_lib() in ${CMAKE_CURRENT_LIST_DIR}: the tree has no game (dagor_add_dng_game)")
  endif()
  set_property(TARGET ${game} APPEND PROPERTY DAGOR_GAME_PULLS ${arg_PULLS})
  foreach(kind INCLUDES SOURCES)
    list(TRANSFORM arg_${kind} PREPEND "${CMAKE_CURRENT_LIST_DIR}/" REGEX "^[^/$][^:]*$")
  endforeach()
  if(arg_INCLUDES)
    target_include_directories(${game} PRIVATE ${arg_INCLUDES})
  endif()
  if(arg_LINK)
    target_link_libraries(${game} PRIVATE ${arg_LINK})
  endif()
  if(arg_SOURCES)
    target_sources(${game} PRIVATE ${arg_SOURCES})
  endif()
endfunction()

# _dagor_game_lib_files(<out-var> <file> <danetgamelibs.txt> <gamelibs.txt>): <file> (_lib.cmake, _aot.cmake) of each lib
# of the lists that has one: the dirs of prog/daNetGameLibs and prog/gameLibs they name, one per line (# comments). A lib
# without the file has only content (scripts, templates, shaders).
function(_dagor_game_lib_files out file dng_libs game_libs)
  set(result)
  foreach(kind DNG GAME)
    if(kind STREQUAL "DNG")
      set(list_file "${dng_libs}")
      set(root daNetGameLibs)
    else()
      set(list_file "${game_libs}")
      set(root gameLibs)
    endif()
    if(NOT list_file)
      continue()
    endif()
    cmake_path(ABSOLUTE_PATH list_file NORMALIZE)
    set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${list_file}")
    file(STRINGS "${list_file}" lines)
    foreach(line IN LISTS lines)
      string(REGEX REPLACE "#.*" "" line "${line}")
      string(STRIP "${line}" line)
      if(NOT line)
        continue()
      endif()
      if(NOT IS_DIRECTORY "${DAGOR_PROG_DIR}/${root}/${line}")
        message(FATAL_ERROR "${list_file}: there is no prog/${root}/${line}")
      endif()
      if(EXISTS "${DAGOR_PROG_DIR}/${root}/${line}/${file}")
        list(APPEND result "${DAGOR_PROG_DIR}/${root}/${line}/${file}")
      endif()
    endforeach()
  endforeach()
  set(${out} "${result}" PARENT_SCOPE)
endfunction()

# --- the project's generated files -------------------------------------------------------------------------------------
# _dagor_game_project_files(<prog dir> <codename> <danetgamelibs.txt> <gamelibs.txt>): the files of the project that its
# lists of libs and its engine make, written when their content changes (all gitignored):
#   _engine.cmd, _engine.sh             DAGOR_ENGINE_ROOT and DAGOR_CDK_DIR (the host's CDK) for develop/ and game/ scripts
#   prog/_libs.vromfs.blk               the libs' scripts and data in the game's vromfs (prog.vromfs.blk includes it)
#   prog/gameBase/gamedata/templates/_libs.entities.blk   their entity templates
#   prog/scripts/_libs_init.das, prog/tools/_libs_init.das  the loading of their daScript, in the game and in the tools
#   prog/shaders/_libs_shaders.blk      their shaders
# and copies their Quirrel stubs (sq_stubs) into stubs/
function(_dagor_game_project_files prog codename dng_libs game_libs)
  cmake_path(GET prog PARENT_PATH root)
  set(header "THIS FILE CREATED BY CODEGEN FROM danetgamelibs.txt AND gamelibs.txt (the CMake configure), DON'T CHANGE IT")
  file(CONFIGURE OUTPUT "${root}/_engine.cmd" NEWLINE_STYLE WIN32 CONTENT
    "@rem ${header}\n@set \"DAGOR_ENGINE_ROOT=${DAGOR_ENGINE_ROOT}\"\n@set \"DAGOR_CDK_DIR=${DAGOR_ENGINE_ROOT}/tools/dagor_cdk/${DAGOR_HOST_TAG}\"\n")
  file(CONFIGURE OUTPUT "${root}/_engine.sh" NEWLINE_STYLE UNIX CONTENT
    "# ${header}\n# source it: . _engine.sh\nexport DAGOR_ENGINE_ROOT=\"${DAGOR_ENGINE_ROOT}\"\nexport DAGOR_CDK_DIR=\"${DAGOR_ENGINE_ROOT}/tools/dagor_cdk/${DAGOR_HOST_TAG}\"\n")

  set(vromfs "")
  set(templates "")
  set(shaders "")
  set(requires "")
  set(loads "")
  foreach(kind DNG GAME)
    if(kind STREQUAL "DNG")
      set(list_file "${dng_libs}")
      set(root_dir "${DAGOR_PROG_DIR}/daNetGameLibs")
      set(mount danetlibs)
    else()
      set(list_file "${game_libs}")
      set(root_dir "${DAGOR_PROG_DIR}/gameLibs")
      set(mount gameLibs)
    endif()
    if(NOT list_file)
      continue()
    endif()
    file(STRINGS "${list_file}" lines)
    foreach(line IN LISTS lines)
      string(REGEX REPLACE "#.*" "" lib "${line}")
      string(STRIP "${lib}" lib)
      if(NOT lib)
        continue()
      endif()
      set(dir "${root_dir}/${lib}")
      cmake_path(GET lib FILENAME name)
      cmake_path(RELATIVE_PATH dir BASE_DIRECTORY "${DAGOR_ENGINE_ROOT}" OUTPUT_VARIABLE engine_rel)
      if(EXISTS "${dir}/${name}_init.das")
        string(REPLACE "/" "." module "${lib}")
        string(APPEND requires "require ${mount}.${module}.${name}_init\n")
        string(APPEND loads "  ok = load_${name}(\"%${mount}/${lib}\") && ok\n")
      endif()
      if(EXISTS "${dir}/_shaders.blk")
        string(APPEND shaders "include \"%engine/${engine_rel}/_shaders.blk\"\n")
      endif()
      file(GLOB lib_templates RELATIVE "${dir}/templates" CONFIGURE_DEPENDS "${dir}/templates/*")
      list(SORT lib_templates)
      foreach(template IN LISTS lib_templates)
        string(APPEND templates "import:t=\"%${mount}/${lib}/templates/${template}\"\n")
      endforeach()
      if(IS_DIRECTORY "${dir}/sq_stubs")
        file(COPY "${dir}/sq_stubs/" DESTINATION "${root}/stubs")
      endif()
      set(wildcards "")
      foreach(ext .blk .das .das_project)
        file(GLOB_RECURSE found CONFIGURE_DEPENDS "${dir}/*${ext}")
        list(FILTER found EXCLUDE REGEX "/_shaders\\.blk$")
        if(found)
          string(APPEND wildcards "  wildcard:t=\"*${ext}\"\n")
        endif()
      endforeach()
      if(wildcards)
        string(APPEND vromfs "\nfolder {\n  output:t=\"${codename}.vromfs.bin\"\n  path:t=\"%engine/${engine_rel}/\"\n"
          "  dest_path:t=\"${mount}/${lib}/\"\n  scan_folder:b=true\n  scan_subfolders:b=true\n${wildcards}}\n")
      endif()
    endforeach()
  endforeach()

  set(let let)
  if(loads)
    set(let var)
  endif()
  set(das_init "options gen2\n\n// ${header}\n\noptions no_aot = true\n${requires}\ndef load_libs() : bool {\n  ${let} ok = true\n${loads}  return ok\n}\n\n[export]\ndef test_all {\n  let ok = load_libs()\n  assert(ok)\n}\n")
  file(CONFIGURE OUTPUT "${prog}/_libs.vromfs.blk" CONTENT "// ${header}\n${vromfs}")
  file(CONFIGURE OUTPUT "${prog}/gameBase/gamedata/templates/_libs.entities.blk" CONTENT "// ${header}\n${templates}")
  file(CONFIGURE OUTPUT "${prog}/shaders/_libs_shaders.blk" CONTENT "// ${header}\n${shaders}")
  file(CONFIGURE OUTPUT "${prog}/scripts/_libs_init.das" CONTENT "${das_init}")
  file(CONFIGURE OUTPUT "${prog}/tools/_libs_init.das" CONTENT "${das_init}")
endfunction()

# --- the game program (prog/daNetGame/game.jam) -----------------------------------------------------------------------
# dagor_add_dng_game(NAME <target> GAME <codename> [WINDOW_TITLE <title>] [USER_DIR <dir>] [MAIN_VROM <path>]
#   [AUTH_KEY_<PLATFORM> <20 bytes>] (PLATFORM: WINDOWS LINUX MACOS ANDROID IOS) [DEDICATED_AUTH <prefix> <platform>...]
#   [LOG_CRYPT_KEY <128 bytes>] [PULLS <pull>...] [DNG_LIBS <danetgamelibs.txt>] [GAME_LIBS <gamelibs.txt>]
#   [AOT_FILES_CMAKE <file>...] <dagor_add_target arguments>)
# The game program: daNetGame's main, the files of FILES_CMAKE, the code game.jam generated (gameproj:: names and paths,
# auth keys, the pull of every module and library) and the libraries of the lists, whose _lib.cmake add what they need
# to it (dagor_game_lib). The client is named <codename>, the dedicated server <codename>-ded. LOG_CRYPT_KEY encrypts
# the logs of Rel and IRel builds with DAGOR_FORCE_LOGS. In the tree of the game's daScript AOT compiler
# (DAGOR_DAS_AOT_COMPILER) it makes <codename>-aot instead, of the files of AOT_FILES_CMAKE and what the libraries'
# _aot.cmake add, and no <target>.
function(dagor_add_dng_game)
  set(key_args)
  foreach(platform WINDOWS LINUX MACOS ANDROID IOS)
    list(APPEND key_args AUTH_KEY_${platform})
  endforeach()
  cmake_parse_arguments(PARSE_ARGV 0 arg "${_DAGOR_TARGET_OPTIONS}"
    "${_DAGOR_TARGET_ONE_VALUE};GAME;WINDOW_TITLE;USER_DIR;MAIN_VROM;DNG_LIBS;GAME_LIBS"
    "${_DAGOR_TARGET_MULTI_VALUE};PULLS;DEDICATED_AUTH;LOG_CRYPT_KEY;AOT_FILES_CMAKE;${key_args}")
  set(target ${arg_NAME})
  if(NOT arg_GAME OR arg_GAME MATCHES "[A-Z]")
    message(FATAL_ERROR "dagor_add_dng_game(${target}): GAME <codename> in lowercase is required (it names the vromfs)")
  endif()
  set(GAME "${arg_GAME}")
  foreach(var WINDOW_TITLE USER_DIR)
    set(${var} "${arg_${var}}")
    if(NOT ${var})
      set(${var} "${GAME}")
    endif()
  endforeach()
  set(MAIN_VROM "${arg_MAIN_VROM}")
  if(NOT MAIN_VROM)
    set(MAIN_VROM "${GAME}.vromfs.bin")
  endif()
  cmake_path(GET MAIN_VROM PARENT_PATH VROM_DIR)
  foreach(var IN LISTS key_args)
    list(LENGTH arg_${var} n)
    if(arg_${var} AND NOT n EQUAL 20)
      message(FATAL_ERROR "dagor_add_dng_game(${target}): ${var} must be 20 bytes, not ${n}")
    endif()
  endforeach()
  set_property(GLOBAL PROPERTY DAGOR_GAME_CODENAME "${GAME}")
  foreach(list DNG_LIBS GAME_LIBS)
    if(arg_${list})
      cmake_path(ABSOLUTE_PATH arg_${list} NORMALIZE)
    endif()
  endforeach()
  _dagor_game_project_files("${CMAKE_CURRENT_SOURCE_DIR}" ${GAME} "${arg_DNG_LIBS}" "${arg_GAME_LIBS}")

  if(DAGOR_DAS_AOT_COMPILER)
    set_property(GLOBAL PROPERTY DAGOR_GAME_TARGET "${GAME}-aot")
    dagor_add_target(NAME ${GAME}-aot EXECUTABLE
      FILES_CMAKE ${arg_AOT_FILES_CMAKE}
      INCLUDE_DIRECTORIES PRIVATE ${DAGOR_DNG_INCLUDES} ${DAGOR_PROG_DIR}/daNetGameLibs ${DAGOR_PROG_DIR}/gameLibs
      BUILD_DEPENDENCIES PRIVATE daNetGame-das-aot Dagor::Quirrel)
    _dagor_game_lib_files(libs _aot.cmake "${arg_DNG_LIBS}" "${arg_GAME_LIBS}")
    foreach(lib IN LISTS libs)
      include("${lib}")
    endforeach()
    return()
  endif()
  if(DAGOR_DAS_AOT)
    _dagor_das_aot_compiler(${GAME} "${CMAKE_CURRENT_SOURCE_DIR}")
  endif()

  set(arg_EXECUTABLE ON)
  set(arg_APPLICATION ON)
  set(arg_OUTPUT_NAME "${GAME}")
  if(DAGOR_DEDICATED)
    set(arg_OUTPUT_NAME "${GAME}-ded")
  endif()
  _dagor_target_arguments(args)
  dagor_add_target(${args})
  set_property(GLOBAL PROPERTY DAGOR_GAME_TARGET "${target}")
  # daNetGame's settings (jam: the game's jamfile included setup.jam): its include dirs, options and physics
  target_include_directories(${target} PRIVATE ${DAGOR_DNG_INCLUDES})
  target_compile_options(${target} PRIVATE ${DAGOR_DNG_OPTIONS})
  target_link_libraries(${target} PRIVATE Dagor::Quirrel Dagor::Phys)

  # gameproj:: and the auth keys: the client's own; the dedicated server's for the clients it checks (outside Rel and
  # IRel unless on Linux, as jam built them)
  set(gen "${CMAKE_CURRENT_BINARY_DIR}/gen/${target}")
  set(CLIENT_ONLY "")
  if(NOT DAGOR_DEDICATED)
    set(CLIENT_ONLY "extern \"C\"\n{\nconst char *dedicated_server_dll_fn = nullptr;\n}")
  endif()
  configure_file("${DAGOR_CMAKE_DIR}/templates/gameproj.cpp.in" "${gen}/gameproj.cpp" @ONLY)
  string(TOUPPER "${DAGOR_PLATFORM}" platform_upper)
  if(arg_AUTH_KEY_${platform_upper})
    list(JOIN arg_AUTH_KEY_${platform_upper} "," key)
    set(PLATFORM_KEY "net::auth_key_t net::get_platform_auth_key()\n{\n  static const uint8_t key[] = {${key}};\n  return auth_key_t(key, sizeof(key));\n}")
  else()
    set(PLATFORM_KEY "net::auth_key_t net::get_platform_auth_key() { return {}; }")
  endif()
  set(SERVER_KEYS "")
  if(DAGOR_DEDICATED)
    set(checked "1")
    if(NOT LINUX)
      set(checked "DAGOR_DBGLEVEL > 0")
    endif()
    set(pairs ${arg_DEDICATED_AUTH})
    set(keys "")
    set(lookups "")
    set(null_defined OFF)
    while(pairs)
      list(POP_FRONT pairs prefix platform)
      string(TOUPPER "${platform}" upper)
      if(arg_AUTH_KEY_${upper})
        list(JOIN arg_AUTH_KEY_${upper} "," key)
        string(APPEND keys "static const uint8_t bkey_${prefix}[] = {${key}};\n"
                           "static net::auth_key_t key_${prefix}{bkey_${prefix}, sizeof(bkey_${prefix})};\n")
        string(APPEND lookups "  if (strstr(pltf, \"${prefix}\") == pltf) { out_key = &key_${prefix}; return true; }\n")
      else()
        if(NOT null_defined)
          string(APPEND keys "static net::auth_key_t key_null;\n")
          set(null_defined ON)
        endif()
        string(APPEND lookups "  if (strstr(pltf, \"${prefix}\") == pltf) { out_key = &key_null; return true; }\n")
      endif()
    endwhile()
    string(CONCAT SERVER_KEYS "#if ${checked}\n${keys}#endif\n"
      "bool net::get_auth_key_for_platform(const char *pltf, net::auth_key_t *&out_key)\n{\n"
      "  if (strstr(pltf, \"win\") == pltf || strstr(pltf, \"mac\") == pltf) { out_key = nullptr; return true; }\n"
      "#if ${checked}\n${lookups}#endif\n  return false;\n}")
  endif()
  configure_file("${DAGOR_CMAKE_DIR}/templates/authKeys.cpp.in" "${gen}/authKeys.cpp" @ONLY)

  # daNetGame's main and version, compiled with the game's include dirs; the GPU switching exports of Windows releases
  file(CONFIGURE OUTPUT "${gen}/gameMain.cpp" CONTENT "#include \"main/main.cpp\"\n")
  file(CONFIGURE OUTPUT "${gen}/gameVersion.cpp" CONTENT "#include \"main/version.cpp\"\n")
  target_sources(${target} PRIVATE "${gen}/gameproj.cpp" "${gen}/authKeys.cpp" "${gen}/gameMain.cpp"
    "${gen}/gameVersion.cpp")
  if(WIN32 AND DAGOR_GAME_RENDERER)
    file(CONFIGURE OUTPUT "${gen}/renderOptimus.cpp" CONTENT "#include \"render/opt/optimus.cpp\"\n")
    target_sources(${target} PRIVATE "$<$<CONFIG:Rel,IRel>:${gen}/renderOptimus.cpp>")
  endif()
  if(arg_LOG_CRYPT_KEY AND DAGOR_FORCE_LOGS)
    list(JOIN arg_LOG_CRYPT_KEY "," key)
    file(CONFIGURE OUTPUT "${gen}/logCryptKey.cpp" CONTENT
      "const unsigned char *get_dagor_log_crypt_key()\n{\n  static const unsigned char key[128] = {${key}};\n  return key;\n}\n")
    target_sources(${target} PRIVATE "$<$<CONFIG:Rel,IRel>:${gen}/logCryptKey.cpp>")
  endif()

  # the pull of every module and library of the game: their dagor_game_lib() calls and the INTERFACE_DAGOR_GAME_PULLS of
  # the libraries it links (pulls of some configurations are $<cond:name>, empty in the others)
  set_property(TARGET ${target} APPEND PROPERTY DAGOR_GAME_PULLS ${arg_PULLS})
  set(pulls "$<FILTER:$<TARGET_GENEX_EVAL:${target},$<TARGET_PROPERTY:${target},DAGOR_GAME_PULLS>>,EXCLUDE,^$>")
  set(bs "\\")
  string(CONCAT text "#include <daECS/core/componentType.h>\n#define REG_SYS${bs}\n"
    "$<$<BOOL:${pulls}>:  RS($<JOIN:${pulls},)${bs}\n  RS(>)${bs}\n>\n"
    "#define RS(x) extern size_t x;\nREG_SYS\n#undef RS\n#define RS(x) + (x)\nsize_t game_pulls = 0 REG_SYS;\n")
  _dagor_generate_source(${target} "${gen}/gamePulls.cpp" "${text}")

  # main/main.cpp, compiled here, shows the splash screen
  if(DAGOR_GAME_RENDERER)
    dagor_game_lib(LINK gameLibs.render.animatedSplashScreen)
  else()
    dagor_game_lib(LINK gameLibs.render.animatedSplashScreen.stub)
  endif()
  dagor_game_lib(INCLUDES "${DAGOR_PROG_DIR}/gameLibs/render/animatedSplashScreen/public_api")

  # what the daNetGameLibs and gameLibs of the lists add to the game: their _lib.cmake (dagor_game_lib)
  _dagor_game_lib_files(libs _lib.cmake "${arg_DNG_LIBS}" "${arg_GAME_LIBS}")
  foreach(lib IN LISTS libs)
    include("${lib}")
  endforeach()
endfunction()
