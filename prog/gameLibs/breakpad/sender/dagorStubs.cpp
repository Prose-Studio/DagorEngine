// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include <perfMon/dag_cpuFreq.h>
#include <util/dag_delayedAction.h>
#include <osApiWrappers/dag_basePath.h>
#include <debug/dag_assert.h>
#include <debug/dag_log.h>
#include <stdlib.h>

// for lockProfiler

void execute_delayed_action_on_main_thread(DelayedAction *, bool, int) {}

const char *dd_get_named_mount_path(const char *, int) { return nullptr; }
const char *dd_resolve_named_mount_in_path(const char *fpath, const char *&mnt_path)
{
  mnt_path = "";
  return fpath;
}

// the kernel's assertion handler (none: a failed assert goes on) and debug log, which osApiWrappers calls outside Rel;
// bpreport has its own log (log.h)
decltype(dgs_assertion_handler) dgs_assertion_handler = nullptr;
#if DAGOR_DBGLEVEL > 0 || DAGOR_FORCE_LOGS
void logmessage_fmt(int, const char *, const DagorSafeArg *, int) {}
#endif
