set(FILES dngBasedRender.cpp dngSkiesSrv.cpp)
set(SourceES renderServicesES.cpp.inl)
set(ES_FILES ${SourceES})
# TODO(jam): if [ GLOB $(Root)/prog/daNetGameLibs/dm : damageEvents.h ] { opt on dngBasedRender.cpp =
#   -DHAVE_DNGLIB_DM ; }
set(SourceES )
