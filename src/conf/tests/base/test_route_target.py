#!/usr/bin/env python

import collections
import types
import unittest
from unittest.mock import Mock
from ipaddress import IPv4Address

from genie.conf import Genie

from genie.libs.conf.bgp import RouteTarget


class test_route_target(unittest.TestCase):

    def test_init(self):

        rt = RouteTarget('1:0')
        self.assertEqual(rt.type, rt.Type.ASN2_index)
        self.assertTupleEqual(rt.fields, (rt.Type.ASN2_index, 1, 0))
        self.assertTupleEqual(rt.bytes, (0, 0, 1, 0, 0, 0, 0))
        self.assertTupleEqual(rt.value_bytes, (0, 1, 0, 0, 0, 0))
        self.assertTupleEqual(rt.value_words, (1, 0, 0))
        self.assertEqual(rt.dotted, '1:0')
        self.assertEqual(rt.dotted_hex3words, '0001.0000.0000')
        self.assertEqual(str(rt), '1:0')
        self.assertEqual(format(rt, ''), '1:0')
        self.assertEqual(format(rt, 'd:d'), '1:0')
        self.assertEqual(format(rt, 'd.d:d'), '1:0')
        self.assertEqual(format(rt, 'x.x.x'), '0001.0000.0000')
        self.assertEqual(rt, RouteTarget(rt.fields))

        rt = RouteTarget('65536:0')
        self.assertEqual(rt.type, rt.Type.ASN4_index)
        self.assertTupleEqual(rt.fields, (rt.Type.ASN4_index, 65536, 0))
        self.assertEqual(rt.dotted, '1.0:0')
        self.assertEqual(rt.dotted_hex3words, '0001.0000.0000')
        self.assertEqual(str(rt), '65536:0')
        self.assertEqual(format(rt, ''), '65536:0')
        self.assertEqual(format(rt, 'd:d'), '65536:0')
        self.assertEqual(format(rt, 'd.d:d'), '1.0:0')
        self.assertEqual(format(rt, 'x.x.x'), '0001.0000.0000')
        self.assertEqual(rt, RouteTarget(rt.fields))

        rt = RouteTarget('1.0:0')
        self.assertEqual(rt.type, rt.Type.ASN4_index)
        self.assertTupleEqual(rt.fields, (rt.Type.ASN4_index, 65536, 0))
        self.assertEqual(str(rt), '65536:0')
        self.assertEqual(rt.dotted, '1.0:0')
        self.assertEqual(rt.dotted_hex3words, '0001.0000.0000')
        self.assertEqual(rt, RouteTarget(rt.fields))

        rt = RouteTarget('1.2.3.4:0')
        self.assertEqual(rt.type, rt.Type.IPv4Address_index)
        self.assertTupleEqual(rt.fields, (rt.Type.IPv4Address_index, IPv4Address('1.2.3.4'), 0))
        self.assertEqual(str(rt), '1.2.3.4:0')
        self.assertEqual(rt.dotted, '1.2.3.4:0')
        self.assertEqual(rt.dotted_hex3words, '0102.0304.0000')
        self.assertEqual(rt, RouteTarget(rt.fields))

        with self.assertRaises(ValueError):
            format(rt, 'blah')

        #with self.assertRaises(ValueError):
        #    rt = RouteTarget('0:0')
        with self.assertRaises(ValueError):
            rt = RouteTarget('5000000000:0')
        with self.assertRaises(ValueError):
            rt = RouteTarget('1:5000000000')
        with self.assertRaises(ValueError):
            rt = RouteTarget('65536:65536')
        with self.assertRaises(ValueError):
            rt = RouteTarget('65536.0:65535')
        with self.assertRaises(ValueError):
            rt = RouteTarget('0.65536:65535')
        with self.assertRaises(ValueError):
            rt = RouteTarget('1.2.3.4:65536')

        rt1 = RouteTarget('1:0')
        rt2 = RouteTarget('1:1')
        rt3 = RouteTarget('1.2.3.4:0')
        rt4 = RouteTarget('1.2.3.4:1')
        rt5 = RouteTarget('65536:0')
        rt6 = RouteTarget('65536:1')
        self.assertEqual(rt1, rt1)
        self.assertNotEqual(rt1, rt2)
        self.assertNotEqual(rt2, rt3)
        self.assertNotEqual(rt3, rt4)
        self.assertNotEqual(rt4, rt5)
        self.assertNotEqual(rt5, rt6)
        self.assertLess(rt1, rt2)
        self.assertLess(rt2, rt3)
        self.assertLess(rt3, rt4)
        self.assertLess(rt4, rt5)
        self.assertLess(rt5, rt6)

if __name__ == '__main__':
    unittest.main()

