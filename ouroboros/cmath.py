"""
A pure python implementation of the standard module library cmath.
"""
import math


" These are constants from float.h"
_FLT_RADIX = 2
_DBL_MIN = 2.2250738585072014e-308
_DBL_MAX = 1.7976931348623157e+308
_DBL_EPSILON = 2.2204460492503131e-16
_DBL_MANT_DIG = 53

_CM_SCALE_UP = 2*int(_DBL_MANT_DIG/2) + 1
_CM_SCALE_DOWN = int(-(_CM_SCALE_UP+1)/2)
_LOG_2 = 0.6931471805599453094
_LOG_10 = 2.302585092994045684
_LARGE_INT = 2305843009213693951
_LOG_LARGE_INT = 18.3628297355029
_LARGE_DOUBLE = 4.49423283715579e+307
_LOG_LARGE_DOUBLE = 307.652655568589
_SQRT_LARGE_DOUBLE = 6.70390396497130e+153
_SQRT_DBL_MIN = 1.49166814624004e-154


e = 2.7182818284590452354
pi = 3.14159265358979323846
tau = 2*pi
inf = float("inf")
infj = complex(0, inf)
nan = float("nan")
nanj = complex(0, nan)


def _make_complex(x):
    if isinstance(x, complex):
        return x
    try:
        z = x.__complex__()
    except AttributeError:
        try:
            z = complex(x.__float__())
        except AttributeError:
            raise TypeError
    if isinstance(z, complex):
        return z
    raise TypeError


def _special_type(x):
    ST_NINF, ST_NEG, ST_NZERO, ST_PZERO, ST_POS, ST_PINF, ST_NAN = range(7)
    if math.isnan(x):
        return ST_NAN
    if math.isfinite(x):
        if x != 0:
            if math.copysign(1, x) == 1:
                return ST_POS
            return ST_NEG
        if math.copysign(1, x) == 1:
            return ST_PZERO
        return ST_NZERO
    if math.copysign(1, x) == 1:
        return ST_PINF
    return ST_NINF


def rect(r, phi):
    _rect_special = [
        [inf+nanj, None, -inf, complex(-float("inf"), -0.0), None, inf+nanj, inf+nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [0, None, complex(-0.0, 0.0), complex(-0.0, -0.0), None, 0, 0],
        [0, None, complex(0.0, -0.0), 0, None, 0, 0],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [inf+nanj, None, complex(float("inf"), -0.0), inf, None, inf+nanj, inf+nanj],
        [nan+nanj, nan+nanj, nan, nan, nan+nanj, nan+nanj, nan+nanj]
    ]

    if not math.isfinite(r) or not math.isfinite(phi):
        if math.isinf(phi) and not math.isnan(r) and r != 0:
            raise ValueError
        if math.isinf(r) and math.isfinite(phi) and phi != 0:
            if r > 0:
                return complex(math.copysign(inf, math.cos(phi)),
                               math.copysign(inf, math.sin(phi)))
            return complex(-math.copysign(inf, math.cos(phi)),
                           -math.copysign(inf, math.sin(phi)))
        return _rect_special[_special_type(r)][_special_type(phi)]
    return complex(r*math.cos(phi), r*math.sin(phi))


def phase(x):
    z = complex(x)
    return math.atan2(z.imag, z.real)


def polar(x):
    return abs(x), phase(x)


def exp(x):
    z = _make_complex(x)

    exp_special = [
        [0+0j, None, complex(0, -0.0), 0+0j, None, 0+0j, 0+0j],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [nan+nanj, None, 1-0j, 1+0j, None, nan+nanj, nan+nanj],
        [nan+nanj, None, 1-0j, 1+0j, None, nan+nanj, nan+nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [inf+nanj, None, complex(float("inf"), -0.0), inf, None, inf+nanj, inf+nanj],
        [nan+nanj, nan+nanj, complex(float("nan"), -0.0), nan, nan+nanj, nan+nanj, nan+nanj]
    ]

    if not isfinite(z):
        if math.isinf(z.real) and math.isfinite(z.imag) and z.imag != 0:
            if z.real > 0:
                ret = complex(math.copysign(inf, math.cos(z.imag)),
                              math.copysign(inf, math.sin(z.imag)))
            else:
                ret = complex(math.copysign(0, math.cos(z.imag)),
                              math.copysign(0, math.sin(z.imag)))
        else:
            ret = exp_special[_special_type(z.real)][_special_type(z.imag)]
        if math.isinf(z.imag) and (math.isfinite(z.real) or
                                   (math.isinf(z.real) and z.real > 0)):
            raise ValueError
        return ret

    if z.real > _LOG_LARGE_DOUBLE:
        ret = e * rect(math.exp(z.real - 1), z.imag)
    else:
        ret = rect(math.exp(z.real), z.imag)
    if math.isinf(ret.real) or math.isinf(ret.imag):
        raise OverflowError
    return ret


def _log(z):
    abs_x = abs(z.real)
    abs_y = abs(z.imag)

    if abs_x > _LARGE_INT or abs_y > _LARGE_INT:
        return complex(math.log(math.hypot(abs_x/2, abs_y/2)) + _LOG_2,
                       math.atan2(z.imag, z.real))
    if abs_x < _DBL_MIN and abs_y < _DBL_MIN:
        if abs_x > 0 or abs_y > 0:
            return complex(math.log(math.hypot(math.ldexp(abs_x, _DBL_MANT_DIG),
                                    math.ldexp(abs_y, _DBL_MANT_DIG)))
                           - _DBL_MANT_DIG * _LOG_2,
                           math.atan2(z.imag, z.real))
        raise ValueError

    rad, phi = polar(z)
    return complex(math.log(rad), phi)


def log(x, base=e):
    if base != e:
        return _log(_make_complex(x))/_log(_make_complex(base))
    return _log(_make_complex(x))


def log10(x):
    z = _log(_make_complex(x))
    return complex(z.real/_LOG_10, z.imag/_LOG_10)


def sqrt(x):
    sqrt_special = [
        [inf-infj, 0-infj, 0-infj, infj, infj, inf+infj, nan+infj],
        [inf-infj, None, None, None, None, inf+infj, nan+nanj],
        [inf-infj, None, 0-0j, 0+0j, None, inf+infj, nan+nanj],
        [inf-infj, None, 0-0j, 0+0j, None, inf+infj, nan+nanj],
        [inf-infj, None, None, None, None, inf+infj, nan+nanj],
        [inf-infj, complex(float("inf"), -0.0), complex(float("inf"), -0.0), inf, inf, inf+infj, inf+nanj],
        [inf-infj, nan+nanj, nan+nanj, nan+nanj, nan+nanj, inf+infj, nan+nanj]
    ]

    z = _make_complex(x)

    if math.isinf(z.real) or math.isinf(z.imag):
        return sqrt_special[_special_type(z.real)][_special_type(z.imag)]

    abs_x, abs_y = abs(z.real), abs(z.imag)
    if abs_x < _DBL_MIN and abs_y < _DBL_MIN:
        if abs_x > 0 or abs_y > 0:
            abs_x = math.ldexp(abs_x, _CM_SCALE_UP)
            s = math.ldexp(math.sqrt(abs_x +
                                     math.hypot(abs_x,
                                                math.ldexp(abs_y,
                                                           _CM_SCALE_UP))),
                           _CM_SCALE_DOWN)
        else:
            return complex(0, z.imag)
    else:
        abs_x /= 8
        s = 2 * math.sqrt(abs_x + math.hypot(abs_x, abs_y/8))

    if z.real >= 0:
        return complex(s, math.copysign(abs_y/(2*s), z.imag))
    return complex(abs_y/(2*s), math.copysign(s, z.imag))


def acos(x):
    _acos_special = [
        [3*pi/4+infj, pi+infj, pi+infj, pi-infj, pi-infj, 3*pi/4-infj, nan+infj],
        [pi/2+infj, None, None, None, None, pi/2-infj, nan+nanj],
        [pi/2+infj, None, None, None, None, pi/2-infj, pi/2+nanj],
        [pi/2+infj, None, None, None, None, pi/2-infj, pi/2+nanj],
        [pi/2+infj, None, None, None, None, pi/2-infj, nan+nanj],
        [pi/4+infj, infj, infj, 0.0-infj, 0.0-infj, pi/4-infj, nan+infj],
        [nan+infj, nan+nanj, nan+nanj, nan+nanj, nan+nanj, nan-infj, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        return _acos_special[_special_type(z.real)][_special_type(z.imag)]

    if abs(z.real) > _LARGE_DOUBLE or abs(z.imag) > _LARGE_DOUBLE:
        if z.real < 0:
            imag = -math.copysign(math.log(math.hypot(z.real/2, z.imag/2)) +
                                  2 * _LOG_2, z.imag)
        else:
            imag = math.copysign(math.log(math.hypot(z.real/2, z.imag/2)) +
                                 2 * _LOG_2, -z.imag)
        return complex(math.atan2(abs(z.imag), z.real), imag)

    s1 = sqrt(complex(1.0 - z.real, -z.imag))
    s2 = sqrt(complex(1.0 + z.real, z.imag))
    return complex(2 * math.atan2(s1.real, s2.real),
                   math.asinh(s2.real*s1.imag - s2.imag*s1.real))


def asin(x):
    z = _make_complex(x)
    z = asinh(complex(-z.imag, z.real))
    return complex(z.imag, -z.real)


def atan(x):
    z = _make_complex(x)
    z = atanh(complex(-z.imag, z.real))
    return complex(z.imag, -z.real)


def cos(x):
    z = _make_complex(x)
    return cosh(complex(-z.imag, z.real))


def sin(x):
    z = _make_complex(x)
    z = sinh(complex(-z.imag, z.real))
    return complex(z.imag, -z.real)


def tan(x):
    z = _make_complex(x)
    z = tanh(complex(-z.imag, z.real))
    return complex(z.imag, -z.real)


def acosh(x):
    z = _make_complex(x)

    if abs(z.real) > _LARGE_DOUBLE or abs(z.imag) > _LARGE_DOUBLE:
        return complex(math.log(math.hypot(z.real/2, z.imag/2)) + 2*_LOG_2,
                       math.atan2(z.imag, z.real))

    s1 = sqrt(complex(z.real-1, z.imag))
    s2 = sqrt(complex(z.real+1, z.imag))
    return complex(math.asinh(s1.real*s2.real + s1.imag*s2.imag),
                   2*math.atan2(s1.imag, s2.real))


def asinh(x):
    _asinh_special = [
        [-inf-1j*pi/4, complex(-float("inf"), -0.0), complex(-float("inf"), -0.0),
            complex(-float("inf"), 0.0), complex(-float("inf"), 0.0), -inf+1j*pi/4, -inf+nanj],
        [-inf-1j*pi/2, None, None, None, None, -inf+1j*pi/2, nan+nanj],
        [-inf-1j*pi/2, None, None, None, None, -inf+1j*pi/2, nan+nanj],
        [inf-1j*pi/2, None, None, None, None, inf+1j*pi/2, nan+nanj],
        [inf-1j*pi/2, None, None, None, None, inf+1j*pi/2, nan+nanj],
        [inf-1j*pi/4, complex(float("inf"), -0.0), complex(float("inf"), -0.0),
            inf, inf, inf+1j*pi/4, inf+nanj],
        [inf+nanj, nan+nanj, complex(float("nan"), -0.0), nan, nan+nanj, inf+nanj, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        return _asinh_special[_special_type(z.real)][_special_type(z.imag)]

    if abs(z.real) > _LARGE_DOUBLE or abs(z.imag) > _LARGE_DOUBLE:
        if z.imag >= 0:
            real = math.copysign(math.log(math.hypot(z.imag/2, z.real/2)) +
                                 2 * _LOG_2, z.real)
        else:
            real = -math.copysign(math.log(math.hypot(z.imag/2, z.real/2)) +
                                  2 * _LOG_2, -z.real)
        return complex(real, math.atan2(z.imag, abs(z.real)))

    s1 = sqrt(complex(1+z.imag, -z.real))
    s2 = sqrt(complex(1-z.imag, z.real))
    return complex(math.asinh(s1.real*s2.imag-s2.real*s1.imag),
                   math.atan2(z.imag, s1.real*s2.real - s1.imag*s2.imag))


def atanh(x):
    _atanh_special = [
        [complex(-0.0, -pi/2), complex(-0.0, -pi/2), complex(-0.0, -pi/2),
            complex(-0.0, pi/2), complex(-0.0, pi/2), complex(-0.0, pi/2),
            complex(-0.0, float("nan"))],
        [complex(-0.0, -pi/2), None, None, None, None, complex(-0.0, pi/2),
            nan+nanj],
        [complex(-0.0, -pi/2), None, None, None, None, complex(-0.0, pi/2),
            complex(-0.0, float("nan"))],
        [-1j*pi/2, None, None, None, None, 1j*pi/2, nanj],
        [-1j*pi/2, None, None, None, None, 1j*pi/2, nan+nanj],
        [-1j*pi/2, -1j*pi/2, -1j*pi/2, 1j*pi/2, 1j*pi/2, 1j*pi/2,  nanj],
        [-1j*pi/2, nan+nanj, nan+nanj, nan+nanj, nan+nanj, 1j*pi/2, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        return _atanh_special[_special_type(z.real)][_special_type(z.imag)]

    if z.real < 0:
        return -atanh(-z)

    ay = abs(z.imag)
    if z.real > _SQRT_LARGE_DOUBLE or ay > _SQRT_LARGE_DOUBLE:
        hypot = math.hypot(z.real/2, z.imag/2)
        return complex(z.real/4/hypot/hypot, -math.copysign(pi/2, -z.imag))
    if z.real == 1 and ay < _SQRT_DBL_MIN:
        if ay == 0:
            raise ValueError
        return complex(-math.log(math.sqrt(ay)/math.sqrt(math.hypot(ay, 2))),
                       math.copysign(math.atan2(2, -ay)/2, z.imag))
    return complex(math.log1p(4*z.real/((1-z.real)*(1-z.real) + ay*ay))/4,
                   -math.atan2(-2*z.imag, (1-z.real)*(1+z.real) - ay*ay)/2)


def cosh(x):
    _cosh_special = [
        [inf+nanj, None, inf, complex(float("inf"), -0.0), None, inf+nanj, inf+nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [nan, None, 1, complex(1, -0.0), None, nan, nan],
        [nan, None, complex(1, -0.0), 1, None, nan, nan],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [inf+nanj, None, complex(float("inf"), -0.0), inf, None, inf+nanj, inf+nanj],
        [nan+nanj, nan+nanj, nan, nan, nan+nanj, nan+nanj, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        if math.isinf(z.imag) and not math.isnan(z.real):
            raise ValueError
        if math.isinf(z.real) and math.isfinite(z.imag) and z.imag != 0:
            if z.real > 0:
                return complex(math.copysign(inf, math.cos(z.imag)),
                               math.copysign(inf, math.sin(z.imag)))
            return complex(math.copysign(inf, math.cos(z.imag)),
                           -math.copysign(inf, math.sin(z.imag)))
        return _cosh_special[_special_type(z.real)][_special_type(z.imag)]

    if abs(z.real) > _LOG_LARGE_DOUBLE:
        x_minus_one = z.real - math.copysign(1, z.real)
        ret = complex(e * math.cos(z.imag) * math.cosh(x_minus_one),
                      e * math.sin(z.imag) * math.sinh(x_minus_one))
    else:
        ret = complex(math.cos(z.imag) * math.cosh(z.real),
                      math.sin(z.imag) * math.sinh(z.real))
    if math.isinf(ret.real) or math.isinf(ret.imag):
        raise OverflowError

    return ret


def sinh(x):

    _sinh_special = [
        [inf+nanj, None, complex(-float("inf"), -0.0), -inf, None, inf+nanj, inf+nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [nanj, None, complex(-0.0, -0.0), complex(-0.0, 0.0), None, nanj, nanj],
        [nanj, None, complex(0.0, -0.0), complex(0.0, 0.0), None, nanj, nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [inf+nanj, None, complex(float("inf"), -0.0), inf, None, inf+nanj, inf+nanj],
        [nan+nanj, nan+nanj, complex(float("nan"), -0.0), nan, nan+nanj, nan+nanj, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        if math.isinf(z.imag) and not math.isnan(z.real):
            raise ValueError
        if math.isinf(z.real) and math.isfinite(z.imag) and z.imag != 0:
            if z.real > 0:
                return complex(math.copysign(inf, math.cos(z.imag)),
                               math.copysign(inf, math.sin(z.imag)))
            return complex(-math.copysign(inf, math.cos(z.imag)),
                           math.copysign(inf, math.sin(z.imag)))
        return _sinh_special[_special_type(z.real)][_special_type(z.imag)]

    if abs(z.real) > _LOG_LARGE_DOUBLE:
        x_minus_one = z.real - math.copysign(1, z.real)
        return complex(math.cos(z.imag) * math.sinh(x_minus_one) * e,
                       math.sin(z.imag) * math.cosh(x_minus_one) * e)
    return complex(math.cos(z.imag) * math.sinh(z.real),
                   math.sin(z.imag) * math.cosh(z.real))


def tanh(x):

    _tanh_special = [
        [-1, None, complex(-1, -0.0), -1, None, -1, -1],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [nan+nanj, None, complex(-0.0, -0.0), complex(-0.0, 0.0), None, nan+nanj, nan+nanj],
        [nan+nanj, None, complex(0.0, -0.0), 0.0, None, nan+nanj, nan+nanj],
        [nan+nanj, None, None, None, None, nan+nanj, nan+nanj],
        [1, None, complex(1, -0.0), 1, None, 1, 1],
        [nan+nanj, nan+nanj, complex(float("nan"), -0.0), nan, nan+nanj, nan+nanj, nan+nanj]
    ]

    z = _make_complex(x)

    if not isfinite(z):
        if math.isinf(z.imag) and math.isfinite(z.real):
            raise ValueError
        if math.isinf(z.real) and math.isfinite(z.imag) and z.imag != 0:
            if z.real > 0:
                return complex(1, math.copysign(0.0, math.sin(z.imag)
                                                * math.cos(z.imag)))
            return complex(-1, math.copysign(0.0, math.sin(z.imag)
                                             * math.cos(z.imag)))
        return _tanh_special[_special_type(z.real)][_special_type(z.imag)]

    if abs(z.real) > _LOG_LARGE_DOUBLE:
        return complex(
            math.copysign(1, z.real),
            4*math.sin(z.imag)*math.cos(z.imag)*math.exp(-2*abs(z.real))
        )
    tanh_x = math.tanh(z.real)
    tan_y = math.tan(z.imag)
    cx = 1/math.cosh(z.real)
    denom = 1 + tanh_x * tanh_x * tan_y * tan_y
    return complex(tanh_x * (1 + tan_y*tan_y)/denom,
                   ((tan_y / denom) * cx) * cx)


def isfinite(x):
    return math.isfinite(x.real) and math.isfinite(x.imag)


def isinf(x):
    return math.isinf(x.real) or math.isinf(x.imag)


def isnan(x):
    return math.isnan(x.real) or math.isnan(x.imag)


def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    a = _make_complex(a)
    b = _make_complex(b)
    rel_tol = float(rel_tol)
    abs_tol = float(abs_tol)
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")
    if a.real == b.real and a.imag == b.imag:
        return True
    if math.isinf(a.real) or math.isinf(a.imag) or math.isinf(b.real) \
            or math.isinf(b.imag):
        return False
    # if isnan(a) or isnan(b):
    #     return False
    diff = abs(a-b)
    return diff <= rel_tol * abs(a) or diff <= rel_tol * abs(b) or diff <= abs_tol
