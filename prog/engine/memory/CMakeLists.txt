# The engine's memory manager. Programs choose its allocator and debug level with the variant they link (jam's global
# UseMemoryAllocator and UseMemoryDebugLevel): engine.memory[.<allocator>[.<debug level>]]
#   <allocator>    default (dlmalloc on Windows without sanitizers, else rtl), rtl, minrtl, dlmalloc, mimalloc, imported
#   <debug level>  default (off in Rel and IRel), off, min, dbg, dbg2
# e.g. engine.memory, engine.memory.rtl, engine.memory.dlmalloc.dbg, engine.memory.default.off
function(_engine_memory allocator debug)
  set(name engine.memory)
  if(NOT debug STREQUAL "default")
    string(APPEND name ".${allocator}.${debug}")
  elseif(NOT allocator STREQUAL "default")
    string(APPEND name ".${allocator}")
  endif()
  if(allocator STREQUAL "default")
    if(DAGOR_SANITIZE STREQUAL "none" AND WIN32)
      set(allocator dlmalloc)
    else()
      set(allocator rtl)
    endif()
  endif()

  set(defines __B_KERNEL_LIB)
  set(includes ${DAGOR_PROG_DIR}/engine/sharedInclude)
  set(deps)

  if(allocator MATCHES "^(rtl|minrtl)$")
    list(APPEND defines USE_RTL_ALLOC)
  elseif(allocator STREQUAL "dlmalloc")
    list(APPEND defines USE_DLMALLOC)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators)
    if(debug MATCHES "^(dbg|dbg2)$")
      list(APPEND deps 3rdPartyLibs.memAllocators.dlmalloc.debug)
    else()
      list(APPEND deps 3rdPartyLibs.memAllocators.dlmalloc)
    endif()
  elseif(allocator STREQUAL "mimalloc")
    # mimalloc's own checks (MI_DEBUG 2) in Dev and Dbg, none with the debug level off (jam's MimDebug)
    list(APPEND includes ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/include
                         ${DAGOR_PROG_DIR}/3rdPartyLibs/memAllocators/mimalloc/mimalloc/include)
    if(debug STREQUAL "off")
      list(APPEND defines USE_MIMALLOC MI_DEBUG=0)
      list(APPEND deps 3rdPartyLibs.memAllocators.mimalloc.nodebug)
    else()
      list(APPEND defines USE_MIMALLOC "MI_DEBUG=$<IF:$<CONFIG:Rel,IRel>,0,2>")
      list(APPEND deps 3rdPartyLibs.memAllocators.mimalloc)
    endif()
  elseif(allocator STREQUAL "imported")
    list(APPEND defines USE_IMPORTED_ALLOC)
  endif()

  if(debug STREQUAL "default")
    list(APPEND defines "$<$<CONFIG:Rel,IRel>:MEM_DEBUGALLOC=-1>")
  else()
    set(level_off -1)
    set(level_min 0)
    set(level_dbg 1)
    set(level_dbg2 2)
    list(APPEND defines MEM_DEBUGALLOC=${level_${debug}})
  endif()

  dagor_add_target(NAME ${name} STATIC
    FILES_CMAKE memory_files.cmake
    INCLUDE_DIRECTORIES PRIVATE ${includes}
    COMPILE_DEFINITIONS PRIVATE ${defines}
    BUILD_DEPENDENCIES PRIVATE ${deps}
  )
endfunction()

foreach(allocator default rtl minrtl dlmalloc mimalloc imported)
  foreach(debug default off min dbg dbg2)
    _engine_memory(${allocator} ${debug})
  endforeach()
endforeach()
