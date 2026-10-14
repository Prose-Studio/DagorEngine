// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include <util/dag_hierBitArray.h>
#include <debug/dag_logSys.h>
#include <utf8/utf8.h>

#define __UNLIMITED_BASE_PATH 1
#include <startup/dag_mainCon.inc.cpp>
#include <stdio.h>
#include <stdlib.h>

// all of Unicode (U+0000..U+10FFFF), a leaf per page of 256 code points
typedef HierConstSizeBitArray<13, ConstSizeBitArray<8>> unicode_range_t;
static constexpr int UNICODE_PAGES = 0x110000 / 256;

int DagorWinMain(bool debugmode)
{
  debug_enable_timestamps(false);
  printf("UTF8 text range detectors\n"
         "Copyright (C) Gaijin Games KFT, 2026\n\n");

  if (dgs_argc < 2)
  {
    printf("\nUsage: utf8ranges-dev.exe arg.utf8.txt [arg1.utf8.txt...]\n");
    return 1;
  }

  unicode_range_t urange;
  Tab<char> utf8(tmpmem);

  for (int i = 1; i < dgs_argc; i++)
  {
    FILE *fp = fopen(dgs_argv[i], "rb");
    if (!fp)
    {
      printf("ERR: cant open utf8 file <%s>\n", dgs_argv[i]);
      return 1;
    }
    fseek(fp, 0, SEEK_END);
    utf8.resize(ftell(fp));
    fseek(fp, 0, SEEK_SET);
    utf8.resize(fread(utf8.data(), 1, utf8.size(), fp));
    fclose(fp);

    const char *p = utf8.data(), *end = p + utf8.size();
    if (!utf8::is_valid(p, end))
    {
      printf("ERR: <%s> is not UTF-8 text\n", dgs_argv[i]);
      return 1;
    }
    // code points, decoded here the same on every platform (wchar_t is UTF-16 on Windows): the characters beyond the
    // BMP land in their own pages, not in those of their UTF-16 surrogates
    while (p < end)
      urange.set(utf8::next(p, end));
  }

  for (int gi = 0; gi < UNICODE_PAGES; gi++)
  {
    int si = 0;
    while (si < 256)
      if (urange.get(gi * 256 + si))
      {
        printf("u%02Xxx\n", gi);
        break;
      }
      else
        si++;
  }
  return 0;
}
