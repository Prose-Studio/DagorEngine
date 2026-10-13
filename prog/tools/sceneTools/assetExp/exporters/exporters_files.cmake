# the exporters in one library (a game's asset manager): static_exp_lib.cpp registers them, the editor code they use is
# stubbed
set(FILES static_exp_lib.cpp exp_skeleton_tools.cpp exp_tools.cpp modelExpUtil.cpp a2dExp.cpp a2dOptimizer.cpp
  animCharExp.cpp exp_animTree.cpp exp_stateGraph.cpp exp_animChar.cpp modelExp.cpp exp_rendInst.cpp exp_dynModel.cpp
  exp_skeleton.cpp exp_rndGrass.cpp exp_collision.cpp fastPhysExp.cpp phObjExp.cpp phSysObj.cpp fxExp.cpp landClsExp.cpp
  locShadersExp.cpp matExp.cpp texExp.cpp exp_impostorData.cpp fxExpStubs.cpp landClsExpStubs.cpp)
