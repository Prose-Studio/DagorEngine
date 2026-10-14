/*  see copyright notice in squirrel.h */
#ifndef _SQPCHEADER_H_
#define _SQPCHEADER_H_

#if defined(_MSC_VER) && defined(_DEBUG)
#include <crtdbg.h>
#endif

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#ifdef QUIRREL_HOST_HEADER
#define _SQ_QHH_STR(x) #x
#define _SQ_QHH_STR2(x) _SQ_QHH_STR(x)
#include _SQ_QHH_STR2(QUIRREL_HOST_HEADER)
#undef _SQ_QHH_STR
#undef _SQ_QHH_STR2
#endif

#include <new>
//squirrel stuff
#include <squirrel.h>
#include "sqobject.h"
#include "sqstate.h"

#if defined(__cpp_lib_to_chars) && __cpp_lib_to_chars >= 201611L
#include <charconv>
#include <float.h>
#include <math.h>
#define SQ_USE_STD_FROM_CHARS 1

// std::from_chars of a float, where a subnormal value is a value: standard libraries that parse through the C library's
// strtof, which sets ERANGE for one, report it out of range. Out of range is a value that rounds to zero (value 0) or
// reaches the largest float (value infinity, as the lexer has it), which the double decides (a process that flushes
// subnormals to zero, fast math, makes any of them a zero float); past the range of double, the exponent's sign does
inline std::from_chars_result sq_float_from_chars(const char *first, const char *last, SQFloat &value)
{
    std::from_chars_result ret = std::from_chars(first, last, value);
    if (ret.ec != std::errc::result_out_of_range || sizeof(SQFloat) != sizeof(float))
        return ret;
    double wide;
    std::from_chars_result wideRet = std::from_chars(first, last, wide);
    if (wideRet.ec == std::errc::result_out_of_range) {
        const char *e = first;
        while (e < wideRet.ptr && *e != 'e' && *e != 'E')
            e++;
        value = (e + 1 < wideRet.ptr && e[1] == '-') ? SQFloat(0) : SQFloat(HUGE_VAL);
        if (*first == '-')
            value = -value;
        return wideRet;
    }
    const double magnitude = fabs(wide);
    if (magnitude >= double(FLT_MAX))
        value = wide < 0 ? -SQFloat(HUGE_VAL) : SQFloat(HUGE_VAL);
    else {
        value = SQFloat(wide);
        if (magnitude > double(FLT_TRUE_MIN) / 2)
            ret.ec = std::errc();
    }
    return ret;
}
#endif

#ifndef SQ_RUNTIME_TYPE_CHECK
#define SQ_RUNTIME_TYPE_CHECK 1
#endif

#ifndef SQ_WATCHDOG_ENABLED
#define SQ_WATCHDOG_ENABLED 0
#endif

#endif //_SQPCHEADER_H_
