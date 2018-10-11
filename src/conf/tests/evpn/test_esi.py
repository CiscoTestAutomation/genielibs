#!/usr/bin/env python

import collections
import types
import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.evpn import ESI
from genie.libs.conf.base import MAC, IPv4Address


class test_esi(unittest.TestCase):

    def test_init(self):

        esi = ESI(0)
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(esi.value, 0)
        self.assertEqual(str(esi), '00:00:00:00:00:00:00:00:00')
        self.assertEqual(esi.dotted, '00.00.00.00.00.00.00.00.00')

        esi = ESI(0, type=1)
        self.assertEqual(esi.type, 1)
        self.assertTupleEqual(esi.bytes, (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(esi.value, 0)
        self.assertEqual(str(esi), '00:00:00:00:00:00:00:00:00')
        self.assertEqual(esi.dotted, '00.00.00.00.00.00.00.00.00')

        esi = ESI('::')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(esi.value, 0)
        self.assertEqual(str(esi), '00:00:00:00:00:00:00:00:00')
        self.assertEqual(esi.dotted, '00.00.00.00.00.00.00.00.00')

        esi = ESI('::1')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (0, 0, 0, 0, 0, 0, 0, 0, 1))
        self.assertEqual(esi.value, 0x000000000000000001)
        self.assertEqual(str(esi), '00:00:00:00:00:00:00:00:01')
        self.assertEqual(esi.dotted, '00.00.00.00.00.00.00.00.01')

        esi = ESI('1::')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (1, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(esi.value, 0x010000000000000000)
        self.assertEqual(str(esi), '01:00:00:00:00:00:00:00:00')
        self.assertEqual(esi.dotted, '01.00.00.00.00.00.00.00.00')

        esi = ESI('1:2::9')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (1, 2, 0, 0, 0, 0, 0, 0, 9))
        self.assertEqual(esi.value, 0x010200000000000009)
        self.assertEqual(str(esi), '01:02:00:00:00:00:00:00:09')
        self.assertEqual(esi.dotted, '01.02.00.00.00.00.00.00.09')

        esi = ESI('01:02:03:04:05:06:07:08:09')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(esi.value, 0x010203040506070809)
        self.assertEqual(str(esi), '01:02:03:04:05:06:07:08:09')
        self.assertEqual(esi.dotted, '01.02.03.04.05.06.07.08.09')

        esi = ESI('01.02.03.04.05.06.07.08.09')
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(esi.value, 0x010203040506070809)
        self.assertEqual(str(esi), '01:02:03:04:05:06:07:08:09')
        self.assertEqual(esi.dotted, '01.02.03.04.05.06.07.08.09')

        esi = ESI('01.02.03.04.05.06.07.08.09.10')
        self.assertEqual(esi.type, 1)
        self.assertTupleEqual(esi.bytes, (2, 3, 4, 5, 6, 7, 8, 9, 16))
        self.assertEqual(esi.value, 0x020304050607080910)
        self.assertEqual(str(esi), '02:03:04:05:06:07:08:09:10')
        self.assertEqual(esi.dotted, '02.03.04.05.06.07.08.09.10')

        esi = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(esi.type, 0)
        self.assertTupleEqual(esi.bytes, (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(esi.value, 0x010203040506070809)
        self.assertEqual(str(esi), '01:02:03:04:05:06:07:08:09')
        self.assertEqual(esi.dotted, '01.02.03.04.05.06.07.08.09')

        esi = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        self.assertEqual(esi.type, 1)
        self.assertTupleEqual(esi.bytes, (2, 3, 4, 5, 6, 7, 8, 9, 10))
        self.assertEqual(esi.value, 0x02030405060708090A)
        self.assertEqual(str(esi), '02:03:04:05:06:07:08:09:0a')
        self.assertEqual(esi.dotted, '02.03.04.05.06.07.08.09.0a')

        esi = ESI(0)
        esi = ESI(0xFFFFFFFFFFFFFFFFFF)
        with self.assertRaises(ValueError):
            esi = ESI(-1)
        with self.assertRaises(ValueError):
            esi = ESI(0x1FFFFFFFFFFFFFFFFFF)

        esi = ESI('::')
        esi = ESI('::9')
        esi = ESI('::2:3:4:5:6:7:8:9')
        esi = ESI('1:2:3:4:5:6:7:8::')
        esi = ESI('1:2:3::7:8:9')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3:4:5:6:7:8:9:10:11')
        with self.assertRaises(ValueError):
            esi = ESI('1.2.3.4.5.6.7.8.9.10.11')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3:4:5:6:7:8')
        with self.assertRaises(ValueError):
            esi = ESI('1.2.3.4.5.6.7.8')
        with self.assertRaises(ValueError):
            esi = ESI('::1:2:3:4:5:6:7:8:9')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3:4:5:6:7:8:9::')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3:4:5::6:7:8:9')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3:4:::6:7:8:9')
        with self.assertRaises(ValueError):
            esi = ESI('1:2:3::5::7:8:9')
        with self.assertRaises(ValueError):
            esi = ESI('::1ff')

        esi = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9))
        with self.assertRaises(TypeError):
            esi = ESI((1, 2, 3, 4, 5, 6, 7, 8))

        esi = ESI(0, type=0)
        esi = ESI(0, type=5)
        with self.assertRaises(ValueError):
            esi = ESI(0, type=-1)
        with self.assertRaises(ValueError):
            esi = ESI(0, type=6)

        esi1 = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9), type=0)
        esi2 = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9), type=0)
        esi3 = ESI((1, 2, 3, 4, 5, 6, 7, 8, 9), type=1)
        esi4 = ESI((1, 2, 3, 4, 5, 6, 7, 8, 10), type=1)
        self.assertEqual(esi1, esi2)
        self.assertNotEqual(esi1, esi3)
        self.assertNotEqual(esi2, esi3)
        self.assertNotEqual(esi3, esi4)
        self.assertLess(esi1, esi3)
        self.assertLess(esi1, esi4)
        self.assertLessEqual(esi1, esi3)
        self.assertLessEqual(esi1, esi2)
        self.assertLessEqual(esi1, esi4)
        self.assertGreater(esi3, esi1)
        self.assertGreater(esi4, esi3)
        self.assertGreater(esi4, esi1)
        self.assertGreaterEqual(esi3, esi1)
        self.assertGreaterEqual(esi4, esi1)
        self.assertGreaterEqual(esi2, esi1)

    def test_create(self):

        esi = ESI.create_type_0('1:2:3:4:5:6:7:8:9')
        self.assertEqual(esi, ESI((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
        self.assertEqual(esi.value, 0x010203040506070809)

        esi = ESI.create_type_1('1:2:3:4:5:6', 0x0708)
        self.assertEqual(esi, ESI((1, 1, 2, 3, 4, 5, 6, 7, 8, 0)))
        self.assertEqual(esi.system_mac, MAC('1:2:3:4:5:6'))
        self.assertEqual(esi.port_key, 0x0708)

        esi = ESI.create_type_2('1:2:3:4:5:6', 0x0708)
        self.assertEqual(esi, ESI((2, 1, 2, 3, 4, 5, 6, 7, 8, 0)))
        self.assertEqual(esi.root_bridge_mac, MAC('1:2:3:4:5:6'))
        self.assertEqual(esi.root_bridge_priority, 0x0708)

        esi = ESI.create_type_3('1:2:3:4:5:6', 0x070809)
        self.assertEqual(esi, ESI((3, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
        self.assertEqual(esi.system_mac, MAC('1:2:3:4:5:6'))
        self.assertEqual(esi.local_discriminator, 0x070809)

        esi = ESI.create_type_4('1.2.3.4', 0x05060708)
        self.assertEqual(esi, ESI((4, 1, 2, 3, 4, 5, 6, 7, 8, 0)))
        self.assertEqual(esi.router_id, IPv4Address('1.2.3.4'))
        self.assertEqual(esi.local_discriminator, 0x05060708)

        esi = ESI.create_type_5(0x01020304, 0x05060708)
        self.assertEqual(esi, ESI((5, 1, 2, 3, 4, 5, 6, 7, 8, 0)))
        self.assertEqual(esi.asn, 0x01020304)
        self.assertEqual(esi.local_discriminator, 0x05060708)

if __name__ == '__main__':
    unittest.main()

