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

    def AssertFractionsEqual(self, a, b):
        """ Here we are checking if 2 fractions are equal.  """

        # firstFrac = Fraction(a, b);
        # secondFrac = Fraction(c, d);

        #First test special edge cases:
        #if we have 0/b, a/0, 0/d, c/0

        #Checking if a == 0 or c == 0 then
        if (a.numerator == 0):
            self.assertEqual(0, a.numerator//a.denominator)
            self.assertEqual(0, _div(a,b))
        else if (b.numerator==0):
            self.assertEqual(0, b.numerator//b.denominator)
            self.assertEqual(0, _div(a,b))

        # Should return nan
        if (a.denominator==0):
            raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
            self.assertEqual(math.is_nan(), _div(a.numerator//a.denominator))
            self.assertEqual(math.is_nan(), _div(a, b))

        if (b.denominator == 0):
            raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
            self.assertEqual(math.is_nan(), _div(b.numerator//b.denominator))
            self.assertEqual(math.is_nan(), _div(a, b))

        if (a.numerator == b.numerator and a.denominator == b.denominator):
            return true
        else: return false

        if (a.numerator * b.denominator == a.denominator * b.numerator):
            return true
        else: return false

    def gcd(a, b):
        """Calculate the Greatest Common Divisor of a and b.

        Unless b==0, the result will have the same sign as b (so that when
        b is divided by it, the result comes out positive).
        """
        while b:
            a, b = b, a%b
        return a

    # Use this function for testing edge cases
    def isPrime(self, a):
        # If given number is greater than 1
        if a > 1:
            # Iterate from 2 to n / 2
            for i in range(2, a//2):
                if (a % i) == 0:
                    return False
                    break
                else:
                    return True
        else:
            return False

    def test_gcd(self, a, b):
        # Testing for gcd: when a == b, when a is a prime, when either a = kb or b = ka
        if (a == b):
            self.assertEqual(test_gcd(a,b),a)

        #If the first is prime then gcd is 1
        if (isPrime(a) or isPrime(b)):
            self.assertEqual(test_gcd(a,b),1)

        #If one is a multiple of the other
        if (__mod__(a, b) == 0):
            self.assertEqual(test_gcd(a,b), a)
        if (__mod__(b, a) == 0):
            self.assertEqual(test_gcd(a,b), b)
