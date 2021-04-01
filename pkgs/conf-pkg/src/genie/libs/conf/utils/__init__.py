'''Library of useful utility functions'''

import itertools as _itertools  # don't export


def round_nearest(value):
    '''Round value to the nearest integer.
    By default, Python rounds to the nearest *even* digit.'''
    return int(value
               + (0.5 if value >= 0 else -0.5))

from math import gcd


def lcm(a, b):
    '''Return lowest common multiple.'''
    return a * b // gcd(a, b)


def nth(iterable, n, default=None):
    '''Returns the nth item or a default value.

    From: Itertools Recipes (https://docs.python.org/3.4/library/itertools.html)
    '''
    return next(_itertools.islice(iterable, n, None), default)

