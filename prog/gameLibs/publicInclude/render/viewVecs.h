//
// Dagor Engine 6.5 - Game Libraries
// Copyright (C) Gaijin Games KFT.  All rights reserved.
//
#pragma once

#include <math/dag_Point4.h>

class TMatrix4;
class TMatrix;

// The camera-relative vectors to the corners of the view (shader vars view_vecLT, ...): directions whose view space z is
// 1, so a position is view_vec * linear depth. A camera's (calc_camera_view_vecs) also has view_ortho_dir, 0 for a
// perspective camera; for an orthographic one the corners are offsets in the plane through the camera and orthoDir is
// its forward axis with w = 1 (a position is view_vec + orthoDir * linear depth, view_vec_to_rel_pos() in viewVecVS.dshl).
struct ViewVecs
{
  Point4 viewVecLT, viewVecRT, viewVecLB, viewVecRB;
  Point4 orthoDir = Point4(0, 0, 0, 0);
};

ViewVecs calc_view_vecs(const TMatrix &view_tm, const TMatrix4 &proj_tm);
// the view vectors of a camera: orthographic ones for an orthographic projection
ViewVecs calc_camera_view_vecs(const TMatrix &view_tm, const TMatrix4 &proj_tm);

void set_viewvecs_to_shader(Point4 &view_vec_lt, Point4 &view_vec_rt, Point4 &view_vec_lb, Point4 &view_vec_rb, const TMatrix &view_tm,
  const TMatrix4 &proj_tm);
void set_viewvecs_to_shader(const Point4 &view_vec_lt, const Point4 &view_vec_rt, const Point4 &view_vec_lb,
  const Point4 &view_vec_rb);
void set_viewvecs_to_shader(const TMatrix &view_tm, const TMatrix4 &proj_tm);
// TODO remove this, uses gettm
void set_viewvecs_to_shader();

// if optional, will not set non-existent variables
void set_inv_globtm_to_shader(const TMatrix4 &view_tm, const TMatrix4 &proj_tm, bool optional);
