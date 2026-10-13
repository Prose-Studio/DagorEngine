// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include "sender.h"


// on Windows called by the WinMain of FLTK's static library, with the command line in UTF-8
int main(int argc, char **argv) { return breakpad::process_report(argc, argv); }
