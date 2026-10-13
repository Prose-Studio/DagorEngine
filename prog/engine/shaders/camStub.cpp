// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include <math/dag_TMatrix.h>

// the camera of mesh streaming (shaderResUnitedData.cpp) in programs that have none of their own (daNetGame's)
const TMatrix &get_cam_itm() { return TMatrix::IDENT; }
