#!/usr/bin/env python

import collections
import types
import unittest
from unittest.mock import Mock

from genie.conf import Genie

from genie.libs.conf.vrf import VpnId


class test_vpn_id(unittest.TestCase):

    def test_init(self):

        vpn_id = VpnId('0:0')
        self.assertEqual(vpn_id.format, vpn_id.Format.OUI_VPN_index)
        self.assertTupleEqual(vpn_id.parts, (0, 0))
        self.assertEqual(str(vpn_id), '0:0')
        self.assertEqual(vpn_id, VpnId(vpn_id.parts))

        vpn_id = VpnId('ffffff:ffffffff')
        self.assertEqual(vpn_id.format, vpn_id.Format.OUI_VPN_index)
        self.assertTupleEqual(vpn_id.parts, (0xffffff, 0xffffffff))
        self.assertEqual(str(vpn_id), 'ffffff:ffffffff')
        self.assertEqual(vpn_id, VpnId(vpn_id.parts))

        with self.assertRaises(ValueError):
            vpn_id = VpnId('fffffff:0')
        with self.assertRaises(ValueError):
            vpn_id = VpnId('0:fffffffff')

        vpn_id1 = VpnId('0:0')
        vpn_id2 = VpnId('ffffff:ffffffff')
        self.assertEqual(vpn_id1, vpn_id1)
        self.assertNotEqual(vpn_id1, vpn_id2)
        self.assertLess(vpn_id1, vpn_id2)

if __name__ == '__main__':
    unittest.main()

