#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

from genie.libs.conf.evpn import Vni


class test_vni(TestCase):

    def test_init(self):

        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr')
        intf1 = Interface(device=dev1, name='GigabitEthernet0/0/0/1')
        intf2 = Interface(device=dev1, name='GigabitEthernet0/0/0/2')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr')
        intf3 = Interface(device=dev2, name='GigabitEthernet0/0/0/3')
        intf4 = Interface(device=dev2, name='GigabitEthernet0/0/0/4')

        with self.assertNoWarnings():

            nve1 = Interface(device=dev1, name='nve1')

            with self.assertRaises(TypeError):
                vni1 = Vni()
            with self.assertRaises(TypeError):
                vni1 = Vni(vni_id=1)
            with self.assertRaises(TypeError):
                vni1 = Vni(nve=nve1)
            vni1 = Vni(nve=nve1, vni_id=1)
            with self.assertRaises(ValueError):
                vni2 = Vni(nve=nve1, vni_id=1)
            vni2 = Vni(nve=nve1, vni_id=2)

            cfg = vni1.build_config(apply=False)
            self.assertMultiLineEqual(str(cfg), '\n'.join([
                "interface nve1",
                " member vni 1",
                "  exit",
                " exit",
                ]))

            cfg = nve1.build_config(apply=False)
            self.assertMultiLineEqual(str(cfg), '\n'.join([
                "interface nve1",
                " member vni 1",
                "  exit",
                " member vni 2",
                "  exit",
                " exit",
                ]))

            cfg = nve1.build_config(apply=False, attributes='vnis__2')
            self.assertMultiLineEqual(str(cfg), '\n'.join([
                "interface nve1",
                " member vni 2",
                "  exit",
                " exit",
                ]))

            cfg = nve1.build_config(apply=False, attributes={
                'vnis': 2,
                })
            self.assertMultiLineEqual(str(cfg), '\n'.join([
                "interface nve1",
                " member vni 2",
                "  exit",
                " exit",
                ]))

            cfg = nve1.build_config(apply=False, attributes={
                'vnis': {
                    vni2: (),
                    },
                })
            self.assertMultiLineEqual(str(cfg), '\n'.join([
                "interface nve1",
                " member vni 2",
                "  exit",
                " exit",
                ]))

if __name__ == '__main__':
    unittest.main()

