// Copyright (C) Gaijin Games KFT.  All rights reserved.

#define INSIDE_RENDERER 1 // fixme: define it for the renderer's sources in the build

#include "private_worldRenderer.h"
void WorldRenderer::setDeformsOrigin(const Point3 &p) { gpuDeformObjectsManager.setOrigin(p); }
void WorldRenderer::createDeforms() { gpuDeformObjectsManager.updateDeforms(); }
void WorldRenderer::closeDeforms() { gpuDeformObjectsManager.close(); }
