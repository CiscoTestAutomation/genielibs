#!/usr/bin/env python

import collections
import types
import unittest
from unittest.mock import Mock

from genie.utils.cisco_collections import typedset

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.evpn import Evpn, Evi


class test_evi(unittest.TestCase):

    def assertDictEqual(self, d1, d2, *args, **kwargs):
        d1_modified = {key:str(value) for key, value in d1.items()}
        return super().assertDictEqual(d1_modified, d2, *args, **kwargs)

    def test_init(self):

        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')

        with self.assertRaises(TypeError):
            evi1 = Evi()

        with self.assertRaises(TypeError):
            evi1 = Evi(device=dev1)

        with self.assertRaises(TypeError):
            evi1 = Evi(evi_id=1)

        with self.assertRaises(AssertionError):
            evi1 = Evi(device=dev1, evi_id=1)

        evpn = Evpn()
        self.assertSetEqual(evpn.evis, set())

        dev2.add_feature(evpn)

        with self.assertRaises(AssertionError):
            evi1 = Evi(device=dev1, evi_id=1)

        dev1.add_feature(evpn)
        evi1 = Evi(device=dev1, evi_id=1)
        self.assertIs(evi1.testbed, testbed)
        self.assertIsInstance(evpn.evis, typedset)
        self.assertSetEqual(evpn.evis, set([evi1]))
        self.assertIs(type(evpn.device_attr[dev1].evis), types.GeneratorType)
        self.assertCountEqual(evpn.device_attr[dev1].evis, [evi1])
        self.assertCountEqual(evpn.device_attr[dev2].evis, [])

        self.assertIsNotNone(evi1.bgp)
        with self.assertRaises(AttributeError):
            evi1.bgp = None

        self.assertIsNotNone(evi1.load_balancing)
        with self.assertRaises(AttributeError):
            evi1.load_balancing = None

        self.assertFalse(evi1.load_balancing.enabled)
        evpn.load_balancing.enabled = True
        self.assertTrue(evi1.load_balancing.enabled)
        with self.assertRaises(AttributeError):
            del evi1.load_balancing.enabled
        evi1.load_balancing.enabled = False
        self.assertFalse(evi1.load_balancing.enabled)
        del evi1.load_balancing.enabled
        self.assertTrue(evi1.load_balancing.enabled)

        cfgs = evpn.build_config(apply=False)
        self.assertDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'evpn',
                ' evi 1',
                '  load-balancing',
                '   exit',
                '  exit',
                ' load-balancing',
                '  exit',
                ' exit',
                ]),
            dev2.name: '\n'.join([
                'evpn',
                ' load-balancing',
                '  exit',
                ' exit',
                ]),
            })

        dev2.remove_feature(evpn)
        cfgs = evpn.build_config(apply=False)
        self.assertDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'evpn',
                ' evi 1',
                '  load-balancing',
                '   exit',
                '  exit',
                ' load-balancing',
                '  exit',
                ' exit',
                ]),
            })

        evi1.load_balancing.enabled = False
        cfgs = evpn.build_config(apply=False)
        self.assertDictEqual(cfgs, {
            dev1.name: '\n'.join([
                'evpn',
                ' evi 1',
                '  exit',
                ' load-balancing',
                '  exit',
                ' exit',
                ]),
            })

        # XXXJST
        # cfg = evi1.build_config(apply=False)
        # self.assertMultiLineEqual(cfg, '\n'.join([
        #     'evpn',
        #     ' evi 1',
        #     '  exit',
        #     ' exit',
        #     ]))

        cfg = evi1.build_config(apply=False)
        self.assertMultiLineEqual(str(cfg), '\n'.join([
            'evi 1',
            ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

