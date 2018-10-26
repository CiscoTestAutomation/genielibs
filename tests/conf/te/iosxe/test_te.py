#!/usr/bin/env python

import unittest,re
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.te import Te, Srlg

class test_te(unittest.TestCase):

    def setUp(self):
        self.tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=self.tb, name='PE1', os='iosxe')
        self.dev2 = Device(testbed=self.tb, name='PE2', os='iosxe')
        self.i1 = Interface(name='GigabitEthernet0/0/1',device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/2',device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/3',device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/4',device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/5',device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/6',device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/7',device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/8',device=self.dev2)
        self.link = Link(name='1_2_1',testbed=self.tb)
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2',testbed=self.tb)
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3',testbed=self.tb)
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4',testbed=self.tb)
        self.link4.connect_interface(interface=self.i7)
        self.link4.connect_interface(interface=self.i8)
        self.assertSetEqual(
            set(self.link.find_interfaces()),
            set([self.i1, self.i2]))
        self.assertSetEqual(
            set(self.dev1.find_interfaces()),
            set([self.i1, self.i3, self.i5, self.i7]))
        self.assertSetEqual(
            set(self.dev2.find_interfaces()),
            set([self.i2, self.i4, self.i6, self.i8]))
    

    def test_MplsTe(self):

        te = Te()
        self.assertSetEqual(set(te.devices), set([]))
        self.assertSetEqual(set(te.links), set([]))


        self.link.add_feature(te)
        self.link2.add_feature(te)
        self.link3.add_feature(te)
        self.link4.add_feature(te)
        self.assertCountEqual(te.devices, [self.dev1, self.dev2])
        self.assertSetEqual(set(te.links), set([self.link, self.link2, self.link3, self.link4]))
        self.assertSetEqual(set(te.interfaces), set([self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8]))


        out = te.build_config(apply=False)

        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls traffic-eng tunnels',
            'interface GigabitEthernet0/0/1',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/3',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/5',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/7',
            ' mpls traffic-eng tunnels',
            ' exit',
        ]))
        
        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'mpls traffic-eng tunnels',
            'interface GigabitEthernet0/0/2',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/4',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/6',
            ' mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/8',
            ' mpls traffic-eng tunnels',
            ' exit',
            ]))


        out = te.build_unconfig(apply=False)


        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'default mpls traffic-eng tunnels',
            'interface GigabitEthernet0/0/1',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/3',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/5',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/7',
            ' default mpls traffic-eng tunnels',
            ' exit',
        ]))
        
        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'default mpls traffic-eng tunnels',
            'interface GigabitEthernet0/0/2',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/4',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/6',
            ' default mpls traffic-eng tunnels',
            ' exit',
            'interface GigabitEthernet0/0/8',
            ' default mpls traffic-eng tunnels',
            ' exit',
            ]))


if __name__ == '__main__':
    unittest.main() 
        
