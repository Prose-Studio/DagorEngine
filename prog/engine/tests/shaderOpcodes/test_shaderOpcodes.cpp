// Copyright (C) Gaijin Games KFT.  All rights reserved.

#include <catch2/catch_test_macros.hpp>
#include <shaders/shOpcodeFormat.h>
#include <EASTL/string.h>
#include <EASTL/vector.h>

// The shader opcode encoders round-trip every value of their fields: the narrow fields in full, the wide ones at their
// edges and in a stride through the range; the opcode byte in full against the parameters' edges, and its edges against
// the parameters, so that no field spills into another.

using namespace shaderopcode;

namespace
{
// the values of the field [lo, hi]: all of them when there are few, else the edges and a stride through the middle
eastl::vector<int> field(int lo, int hi)
{
  eastl::vector<int> v;
  for (int x = lo; x <= hi; x += (hi - lo < 1024 || x < lo + 256 || x > hi - 256) ? 1 : 97)
    v.push_back(x);
  return v;
}

const eastl::vector<int> all_ops = field(0, 0xFF);
const int edge_ops[] = {0, 1, 0x7F, 0x80, 0xFE, 0xFF};
// the edges of a signed field whose all-ones value is -1, and of the parameters of op2 and op3
const int edges8[] = {-1, 0, 1, 0x55, 0x7F, 0x80, 0xFE};

// the first mismatch of a sweep: kept until the end, where the case checks that there was none
struct Mismatch
{
  eastl::string what;
  void operator()(bool ok, const char *fmt, int a, int b = 0, int c = 0, int d = 0)
  {
    if (!ok && what.empty())
      what.sprintf(fmt, a, b, c, d);
  }
};
} // namespace

TEST_CASE("op0 and op1 keep the opcode and the 16-bit parameter", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int op : all_ops)
  {
    bad(getOp(makeOp0(op)) == op, "op0(%d)", op);
    for (int p1 : field(-1, 0xFFFE))
    {
      uint32_t c = makeOp1(op, p1);
      bad(getOp(c) == op && getOp1p1s(c) == p1, "op1(%d, %d)", op, p1);
    }
  }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}

TEST_CASE("op2 keeps the 10-bit and 14-bit parameters, op2_8_16 the 8-bit and 16-bit ones", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int op : edge_ops)
    for (int p1 : field(-1, 0x3FE))
      for (int p2 : field(-1, 0x3FFE))
      {
        uint32_t c = makeOp2(op, p1, p2);
        bad(getOp(c) == op && getOp2p1s(c) == p1 && getOp2p2s(c) == p2, "op2(%d, %d, %d)", op, p1, p2);
      }
  for (int op : all_ops)
    for (int p1 : field(-1, 0xFE))
      for (int p2 : {-1, 0, 1, 0x7FFF, 0x8000, 0xFFFE})
      {
        uint32_t c = makeOp2_8_16(op, p1, p2);
        bad(getOp(c) == op && getOp2p1_8(c) == uint32_t(p1 & 0xFF) && getOp2p2_16(c) == uint32_t(p2 & 0xFFFF), "op2_8_16(%d, %d, %d)",
          op, p1, p2);
      }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}

TEST_CASE("op3 keeps its three 8-bit parameters", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int p1 = -1; p1 < 0xFF; p1++) // every combination, with one opcode
    for (int p2 = -1; p2 < 0xFF; p2++)
      for (int p3 = -1; p3 < 0xFF; p3++)
      {
        uint32_t c = makeOp3(0xA5, p1, p2, p3);
        bad(getOp(c) == 0xA5 && getOp3p1s(c) == p1 && getOp3p2s(c) == p2 && getOp3p3s(c) == p3, "op3(0xA5, %d, %d, %d)", p1, p2, p3);
      }
  for (int op : all_ops)
    for (int p1 : edges8)
      for (int p2 : edges8)
        for (int p3 : edges8)
        {
          uint32_t c = makeOp3(op, p1, p2, p3);
          bad(getOp(c) == op && getOp3p1s(c) == p1 && getOp3p2s(c) == p2 && getOp3p3s(c) == p3, "op3(%d, %d, %d, %d)", op, p1, p2, p3);
        }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}

TEST_CASE("the stage/slot and function call opcodes keep their fields", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int op : edge_ops)
    for (int stage = 0; stage <= 7; stage++)
      for (int slot = 0; slot <= 0x7F; slot++)
        for (int ofs : field(0, 0x3FFF))
        {
          uint32_t c = makeOpStageSlot(op, stage, slot, ofs);
          bad(getOp(c) == op && getOpStageSlot_Stage(c) == stage && getOpStageSlot_Slot(c) == slot && getOpStageSlot_Reg(c) == ofs,
            "stage_slot(%d, %d, %d, %d)", op, stage, slot, ofs);
        }
  for (int op : edge_ops)
    for (int fid = 0; fid < 64; fid++)
      for (int reg : field(0, 0x3FFF))
        for (int args = 0; args < 16; args++)
        {
          uint32_t c = makeOpFunctionCall(op, fid, reg, args);
          bad(getOp(c) == op && getOpFunctionCall_FuncId(c) == fid && getOpFunctionCall_OutReg(c) == reg &&
                getOpFunctionCall_ArgCount(c) == args,
            "function_call(%d, %d, %d, %d)", op, fid, reg, args);
        }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}

TEST_CASE("patching an op2 parameter keeps the rest of the opcode", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int op : edge_ops)
    for (int p1 : {-1, 0, 0x155, 0x3FE})
      for (int p2 : field(-1, 0x3FFE))
      {
        uint32_t c = patchOp2p2(makeOp2(op, p1, 0x1234), p2);
        bad(getOp(c) == op && getOp2p1s(c) == p1 && getOp2p2s(c) == p2, "patchOp2p2(op2(%d, %d, _), %d)", op, p1, p2);
      }
  for (int op : edge_ops)
    for (int p2 : {-1, 0, 0x7FFF, 0xFFFE})
      for (int p1 : field(-1, 0xFE))
      {
        uint32_t c = patchOp2p1_8(makeOp2_8_16(op, 0x5A, p2), p1);
        bad(getOp(c) == op && getOp2p1_8(c) == uint32_t(p1 & 0xFF) && getOp2p2_16(c) == uint32_t(p2 & 0xFFFF),
          "patchOp2p1_8(op2_8_16(%d, _, %d), %d)", op, p2, p1);
      }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}

TEST_CASE("data2 keeps its two 16-bit words, data4 its four bytes", "[shaders][opcodes]")
{
  Mismatch bad;
  for (int p1 : field(-1, 0xFFFE))
    for (int p2 : field(-1, 0xFFFE))
    {
      uint32_t d = makeData2(p1, p2);
      TwoWords w = unpackData2(d);
      bad(getData2p1s(d) == p1 && getData2p2s(d) == p2 && w.lo == uint16_t(p1) && w.hi == uint16_t(p2), "data2(%d, %d)", p1, p2);
    }
  for (int p1 = -1; p1 < 0xFF; p1++)
    for (int p2 = -1; p2 < 0xFF; p2++)
      for (int p3 : edges8)
        for (int p4 : edges8)
        {
          uint32_t d = makeData4(p1, p2, p3, p4);
          FourBytes b = unpackData4(d);
          bad(getData4p1(d) == uint32_t(p1 & 0xFF) && getData4p2(d) == uint32_t(p2 & 0xFF) && getData4p3(d) == uint32_t(p3 & 0xFF) &&
                getData4p4(d) == uint32_t(p4 & 0xFF) && b.b1 == uint8_t(p1) && b.b2 == uint8_t(p2) && b.b3 == uint8_t(p3) &&
                b.b4 == uint8_t(p4),
            "data4(%d, %d, %d, %d)", p1, p2, p3, p4);
        }
  INFO(bad.what.c_str());
  REQUIRE(bad.what.empty());
}
