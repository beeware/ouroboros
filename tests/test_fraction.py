import os
import sys
import sysconfig
import unittest
import math
import fractions
import math
import numbers
import operator
import re
import sys

from decimal import Decimal
from test.support import requires_IEEE_754
import ouroboros.fractions as fraction
from ouroboros.fractions import *

INF = float('inf')
NAN = float('nan')
NINF = float('-inf')

# find file with test values
if __name__ == '__main__':
    file = sys.argv[0]
else:
    file = __file__
test_dir = os.path.dirname(file) or os.curdir
test_file = os.path.join(test_dir, 'fractions_testcases.txt')

class fractionsTests(unittest.TestCase):
    # list of all functions in fractions
    test_functions = [getattr(fractions, fname) for fname in [
            'gcd', 'from_float', 'from_decimal', 'limit_denominator', 'forward', 'reverse',
            '_add', '_sub', '_mul', '_div', '__floordiv__', '__mod__', '__pow__']]

    def setUp(self):
        self.test_values = open(test_file)

    def tearDown(self):
        self.test_values.close()

    #Testing to see if x and y are equal
    def assertFloatIdentical(self, x, y):
        """Fail unless floats x and y are identical, in the sense that:
        (1) both x and y are nans, or
        (2) both x and y are infinities, with the same sign, or
        (3) both x and y are zeros, with the same sign, or
        (4) x and y are both finite and nonzero, and x == y
        """
        msg = 'floats {!r} and {!r} are not identical'

        if math.isnan(x) or math.isnan(y):
            if math.isnan(x) and math.isnan(y):
                return
        elif x == y:
            if x != 0.0:
                return
            # both zero; check that signs match
            elif math.copysign(1.0, x) == math.copysign(1.0, y):
                return
            else:
                msg += ': zeros have different signs'
        self.fail(msg.format(x, y))

    def AssertFractionsEqual(self, a, b, c, d, rel_err=2e-15, abs_err=5e-323, msg=None):
        """ Here we are checking if 2 fractions are equal. The fractions are
        a/b and c/d """

        firstFrac = __new__(a, b)
        secondFrac = __new__(c, d)

        #First test special edge cases:
        #if we have 0/b, a/0, 0/d, c/0

        #Checking if a == 0 or c == 0 then
        if (a == 0):
            self.assertEqual(0, a//b)
            self.assertEqual(0, _div(firstFrac, secondFrac))
        else if (c==0):
            self.assertEqual(0, c//d)
            self.assertEqual(0, _div(firstFrac, secondFrac))

        # Should return nan
        if (b==0):
            self.assertEqual(math.is_nan(), _div(a//b))
            self.assertEqual(math.is_nan(), _div(firstFrac, secondFrac))

        if (d == 0):
            self.assertEqual(math.is_nan(), _div(c//d))
            self.assertEqual(math.is_nan(), _div(firstFrac, secondFrac))


    def rAssertAlmostEqual(self, a, b, rel_err = 2e-15, abs_err = 5e-323,
                           msg=None):
        """Fail if the two floating-point numbers are not almost equal.

        Determine whether floating-point values a and b are equal to within
        a (small) rounding error.  The default values for rel_err and
        abs_err are chosen to be suitable for platforms where a float is
        represented by an IEEE 754 double.  They allow an error of between
        9 and 19 ulps.
        """

        # special values testing
        if math.isnan(a):
            if math.isnan(b):
                return
            self.fail(msg or '{!r} should be nan'.format(b))

        if math.isinf(a):
            if a == b:
                return
            self.fail(msg or 'finite result where infinity expected: '
                      'expected {!r}, got {!r}'.format(a, b))

        # if both a and b are zero, check whether they have the same sign
        # (in theory there are examples where it would be legitimate for a
        # and b to have opposite signs; in practice these hardly ever
        # occur).
        if not a and not b:
            if math.copysign(1., a) != math.copysign(1., b):
                self.fail(msg or 'zero has wrong sign: expected {!r}, '
                          'got {!r}'.format(a, b))

        # if a-b overflows, or b is infinite, return False.  Again, in
        # theory there are examples where a is within a few ulps of the
        # max representable float, and then b could legitimately be
        # infinite.  In practice these examples are rare.
        try:
            absolute_error = abs(b-a)
        except OverflowError:
            pass
        else:
            # test passes if either the absolute error or the relative
            # error is sufficiently small.  The defaults amount to an
            # error of between 9 ulps and 19 ulps on an IEEE-754 compliant
            # machine.
            if absolute_error <= max(abs_err, rel_err * abs(a)):
                return
        self.fail(msg or
                  '{!r} and {!r} are not sufficiently close'.format(a, b))



    def gcd(a, b):
        """Calculate the Greatest Common Divisor of a and b.

        Unless b==0, the result will have the same sign as b (so that when
        b is divided by it, the result comes out positive).
        """
        while b:
            a, b = b, a%b
        return a

    def test_values(self, )
    def test_gcd(self, a, b):
        self.rAssertAlmostEqual()
        self.assertFalse(cmath.isnan(1))
        self.assertFalse(cmath.isnan(1j))
        self.assertFalse(cmath.isnan(INF))
        self.assertTrue(cmath.isnan(NAN))
        self.assertTrue(cmath.isnan(complex(NAN, 0)))
        self.assertTrue(cmath.isnan(complex(0, NAN)))
        self.assertTrue(cmath.isnan(complex(NAN, NAN)))
        self.assertTrue(cmath.isnan(complex(NAN, INF)))
        self.assertTrue(cmath.isnan(complex(INF, NAN)))
