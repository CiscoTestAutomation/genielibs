#!/usr/bin/env python

import unittest
from unittest.mock import Mock
import re

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.ldp import Ldp
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.access_list import AccessList
from genie.libs.conf.base.neighbor import IPv4LsrNeighbor, IPv6Neighbor, IPLsrNeighborSubAttributes



class test_ldp(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        tb = Genie.testbed = Testbed()
        self.dev1 = Device(testbed=tb, name='PE1', os='iosxe')
        self.dev2 = Device(testbed=tb, name='PE2', os='iosxe')
        self.i1 = Interface(name='GigabitEthernet0/0/1', device=self.dev1)
        self.i2 = Interface(name='GigabitEthernet0/0/2', device=self.dev2)
        self.i3 = Interface(name='GigabitEthernet0/0/3', device=self.dev1)
        self.i4 = Interface(name='GigabitEthernet0/0/4', device=self.dev2)
        self.i5 = Interface(name='GigabitEthernet0/0/5', device=self.dev1)
        self.i6 = Interface(name='GigabitEthernet0/0/6', device=self.dev2)
        self.i7 = Interface(name='GigabitEthernet0/0/7', device=self.dev1)
        self.i8 = Interface(name='GigabitEthernet0/0/8', device=self.dev2)
        self.link = Link(name='1_2_1')
        self.link.connect_interface(interface=self.i1)
        self.link.connect_interface(interface=self.i2)
        self.link2 = Link(name='1_2_2')
        self.link2.connect_interface(interface=self.i3)
        self.link2.connect_interface(interface=self.i4)
        self.link3 = Link(name='1_2_3')
        self.link3.connect_interface(interface=self.i5)
        self.link3.connect_interface(interface=self.i6)
        self.link4 = Link(name='1_2_4')
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

    def test_01_interface_only(self):

        ldp = Ldp()
        self.assertSetEqual(set(ldp.devices), set([]))
        self.assertSetEqual(set(ldp.links), set([]))


        self.link.add_feature(ldp)
        self.link2.add_feature(ldp)
        self.link3.add_feature(ldp)
        self.link4.add_feature(ldp)
        self.assertCountEqual(ldp.devices, [self.dev1, self.dev2])
        self.assertSetEqual(set(ldp.links), set([self.link, self.link2, self.link3, self.link4]))
        self.assertSetEqual(set(ldp.interfaces), set([self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8]))

        # ==Test interface-only config==
        out = ldp.build_config(apply=False)
        if 1:
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/1')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/3')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/5')
            self.assertRegex(str(out['PE1']), 'interface GigabitEthernet0/0/7')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/2')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/4')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/6')
            self.assertRegex(str(out['PE2']), 'interface GigabitEthernet0/0/8')

    def test_1_top_level(self):

        acl1 = AccessList(name='1')
        acl2 = AccessList(name='2')
        acl3 = AccessList(name='3')
        acl4 = AccessList(name='4')
        acl5 = AccessList(name='5')
        acl6 = AccessList(name='6')
        acl7 = AccessList(name='7')
        acl8 = AccessList(name='8')
        acl9 = AccessList(name='9')
        acl11 = AccessList(name='11')
        acl22 = AccessList(name='22')
        acl33 = AccessList(name='33')
        acl44 = AccessList(name='44')

        ldp = Ldp()
        self.link.add_feature(ldp)

        # ==Test top-level config==
        ldp.hello_holdtime = 100
        ldp.hello_interval = 200
        ldp.targeted_hello_accept = True
        ldp.gr = True
        ldp.gr_fwdstate_holdtime = 60
        ldp.nsr = True
        ldp.device_attr['PE1'].session_holdtime = 444
        ldp.session_protection = True
        ldp.session_protection_dur = 222
        ldp.device_attr['PE2'].session_protection_dur = 333
        ldp.session_protection_for_acl = acl1

        out = ldp.build_config(apply=False)
        if 1:
            self.assertCountEqual(out.keys(), ['PE1', 'PE2'])
            self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
                'mpls label protocol ldp',
                'mpls ip',
                'mpls ldp nsr',
                'mpls ldp graceful-restart',
                'mpls ldp graceful-restart timers forwarding-holding 60',
                'mpls ldp discovery hello interval 200',
                'mpls ldp discovery hello holdtime 100',
                'mpls ldp discovery targeted-hello accept',
                'mpls ldp session protection for 1 222',
                'interface GigabitEthernet0/0/1',
                ' mpls ip',
                ' exit',
            ]))

            self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
                'mpls label protocol ldp',
                'mpls ip',
                'mpls ldp nsr',
                'mpls ldp graceful-restart',
                'mpls ldp graceful-restart timers forwarding-holding 60',
                'mpls ldp discovery hello interval 200',
                'mpls ldp discovery hello holdtime 100',
                'mpls ldp discovery targeted-hello accept',
                'mpls ldp session protection for 1 333',
                'interface GigabitEthernet0/0/2',
                ' mpls ip',
                ' exit',
            ]))

        if 1:
            # set the per-attr variables that are inherited by VRF
            ldp.device_attr['PE1'].vrf_attr['default'].router_id = self.i1
            ldp.device_attr['PE2'].vrf_attr['default'].router_id = self.i2

            out = ldp.build_config(apply=False)
            self.assertRegex(str(out['PE1']), 'router-id GigabitEthernet0/0/1')

            self.assertRegex(str(out['PE2']), 'router-id GigabitEthernet0/0/2')

        # Check unconfig - <nsr> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__nsr')
        if 1:
            self.assertRegex(str(out['PE1']), 'no mpls ldp nsr')
            self.assertRegex(str(out['PE2']), 'no mpls ldp nsr')

        # Check unconfig - <gr> config filter=
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__gr')
        if 1:
            self.assertRegex(str(out['PE1']), 'no mpls ldp graceful-restart')
            self.assertRegex(str(out['PE2']), 'no mpls ldp graceful-restart')

    def test_2_per_vrf(self):

        acl1 = AccessList(name='1')
        acl2 = AccessList(name='2')
        acl3 = AccessList(name='3')
        acl4 = AccessList(name='4')
        acl5 = AccessList(name='5')
        acl6 = AccessList(name='6')
        acl7 = AccessList(name='7')
        acl8 = AccessList(name='8')
        acl9 = AccessList(name='9')
        acl11 = AccessList(name='11')
        acl22 = AccessList(name='22')
        acl33 = AccessList(name='33')
        acl44 = AccessList(name='44')

        ldp = Ldp()
        self.link.add_feature(ldp)
        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        vrf2 = Vrf(name='vrf2')
        ldp.add_force_vrf(vrf2)
        ldp.device_attr['PE1'].router_id = self.i1
        ldp.device_attr['PE2'].router_id = self.i2
        ldp.device_attr['PE1'].vrf_attr['vrf1'].router_id = self.i3
        ldp.device_attr['PE2'].vrf_attr['vrf1'].router_id = self.i4

        # Test per vrf config
        
        # Check vrf config - full config
        out = ldp.build_config(apply=False)

        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls label protocol ldp',
            'mpls ip',
            'mpls ldp router-id GigabitEthernet0/0/1',
            'mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3',
            'interface GigabitEthernet0/0/1',
            ' mpls ip',
            ' exit',
        ]))


        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'mpls label protocol ldp',
            'mpls ip',
            'mpls ldp router-id GigabitEthernet0/0/2',
            'mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4',
            'interface GigabitEthernet0/0/2',
            ' mpls ip',
            ' exit',
        ]))


        # Test VRF unconfig
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr')
        self.assertTrue('no mpls ldp router-id GigabitEthernet0/0/1' in str(out['PE1']))
        self.assertTrue('no mpls ldp router-id GigabitEthernet0/0/2' in str(out['PE2']))
        self.assertTrue('no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3' in str(out['PE1']))
        self.assertTrue('no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4' in str(out['PE2']))

        out2 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr')
        self.assertTrue('mpls ldp router-id GigabitEthernet0/0/1' in str(out2['PE1']))
        self.assertTrue('mpls ldp router-id GigabitEthernet0/0/2' in str(out2['PE2']))
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3' in str(out2['PE1']))
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4' in str(out2['PE2']))

        # Check vrf config - vrf <vrf1> config filter
        out3 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__vrf1')
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3' in str(out3['PE1']))
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4' in str(out3['PE2']))
        # interface output from default vrf should not be built
        self.assertNotRegex(str(out['PE1']), '(?s)interface Gig')

        # Check vrf unconfig - vrf <vrf1> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__vrf1')
        self.assertEqual(str(out['PE1']), 'no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3')
        self.assertEqual(str(out['PE2']), 'no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4')

        # Check vrf unconfig - vrf <vrf1> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__router_id')
        self.assertTrue('no mpls ldp router-id GigabitEthernet0/0/1' in str(out['PE1']))
        self.assertTrue('no mpls ldp router-id GigabitEthernet0/0/2' in str(out['PE2']))
        self.assertTrue('no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3' in str(out['PE1']))
        self.assertTrue('no mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4' in str(out['PE2']))

        # Check vrf unconfig - vrf <vrf1> config filter after adding router-id to vrf2
        ldp.device_attr['PE2'].vrf_attr['vrf2'].router_id = self.i6
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__router_id')
        self.assertTrue('mpls ldp router-id GigabitEthernet0/0/1' in str(out['PE1']))
        self.assertTrue('mpls ldp router-id GigabitEthernet0/0/2' in str(out['PE2']))
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/3' in str(out['PE1']))
        self.assertTrue('mpls ldp router-id vrf vrf1 GigabitEthernet0/0/4' in str(out['PE2']))
        self.assertTrue('mpls ldp router-id vrf vrf2 GigabitEthernet0/0/6' in str(out['PE2']))


        # Check vrf config - vrf <vrf2> config filter
        out3 = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__vrf2')
        self.assertEqual(str(out3['PE2']) ,'mpls ldp router-id vrf vrf2 GigabitEthernet0/0/6')

    def test_3_per_intf(self):

        acl1 = AccessList(name='1')
        acl2 = AccessList(name='2')
        acl3 = AccessList(name='3')
        acl4 = AccessList(name='4')
        acl5 = AccessList(name='5')
        acl6 = AccessList(name='6')
        acl7 = AccessList(name='7')
        acl8 = AccessList(name='8')
        acl9 = AccessList(name='9')
        acl11 = AccessList(name='11')
        acl22 = AccessList(name='22')
        acl33 = AccessList(name='33')
        acl44 = AccessList(name='44')

        ldp = Ldp()
        self.link.add_feature(ldp)
        self.link4.add_feature(ldp)

        ldp.hello_interval = 88
        ldp.device_attr['PE2'].hello_holdtime = 99


        # ==Test per interface config===
        out = ldp.build_config(apply=False)
        if 1:

            self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
                'mpls label protocol ldp',
                'mpls ip',
                'mpls ldp discovery hello interval 88',
                'interface GigabitEthernet0/0/1',
                ' mpls ip',
                ' exit',
                'interface GigabitEthernet0/0/7',
                ' mpls ip',
                ' exit',
            ]))


            self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
                'mpls label protocol ldp',
                'mpls ip',
                'mpls ldp discovery hello interval 88',
                'mpls ldp discovery hello holdtime 99',
                'interface GigabitEthernet0/0/2',
                ' mpls ip',
                ' exit',
                'interface GigabitEthernet0/0/8',
                ' mpls ip',
                ' exit',
            ]))

        # Check intf unconfig - intf <GigabitEthernet0/0/0/8> config filter
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__interface_attr__GigabitEthernet0/0/8')
        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'interface GigabitEthernet0/0/8',
            ' no mpls ip',
            ' exit',
        ]))


    def test_4_per_neighbor(self):

        ldp = Ldp()
        self.link.add_feature(ldp)
        nbr1 = IPv4LsrNeighbor('1.2.3.4:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.6:0')
        

        ldp.device_attr['PE1'].password = 'password1'
        ldp.device_attr['PE2'].password = '060506324F41'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbors = [nbr1, nbr2, nbr3]
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr2].password = 'blah'
        ldp.device_attr['PE1'].vrf_attr['default'].neighbor_attr[nbr3].password = '060506324F41'

        # ==Test per neighbor config==
        out = ldp.build_config(apply=False)

        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls label protocol ldp',
            'mpls ip',
            'mpls ldp neighbor 1.2.3.4 password password1',
            'mpls ldp neighbor 1.2.3.5 password blah',
            'mpls ldp neighbor 1.2.3.6 password 060506324F41',
            'interface GigabitEthernet0/0/1',
            ' mpls ip',
            ' exit',
        ]))


        self.assertMultiLineEqual(str(out['PE2']), '\n'.join([
            'mpls label protocol ldp',
            'mpls ip',
            'interface GigabitEthernet0/0/2',
            ' mpls ip',
            ' exit',
        ]))

        # Check nbr config - nbr <1.2.3.5:0'> config filter
        out = ldp.build_config(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.5:0')
        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls ldp neighbor 1.2.3.5 password blah',
        ]))

        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.5:0__password')
        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'no mpls ldp neighbor 1.2.3.5 password blah',
        ]))
   
        out = ldp.build_unconfig(apply=False, attributes='device_attr__*__vrf_attr__*__neighbor_attr__1.2.3.6:0__password')
        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'no mpls ldp neighbor 1.2.3.6 password 060506324F41',
        ]))

    def test_8_per_vrf_per_neighbor(self):

        ldp = Ldp()
        self.link.add_feature(ldp)
        vrf = Vrf(name='vrf1')
        ldp.add_force_vrf(vrf)
        nbr1 = IPv4LsrNeighbor('1.2.3.4:0')
        nbr2 = IPv4LsrNeighbor('1.2.3.5:0')
        nbr3 = IPv4LsrNeighbor('1.2.3.6:0')

        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbors = [nbr1, nbr2, nbr3]
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.5:0'].password = 'blah22'
        ldp.device_attr['PE1'].vrf_attr['vrf1'].neighbor_attr['1.2.3.6:0'].password = '060506324F41'

        # ==Test per vrf per neighbor config==
        out = ldp.build_config(apply=False)

        self.assertMultiLineEqual(str(out['PE1']), '\n'.join([
            'mpls label protocol ldp',
            'mpls ip',
            'mpls ldp neighbor vrf vrf1 1.2.3.5 password blah22',
            'mpls ldp neighbor vrf vrf1 1.2.3.6 password 060506324F41',
            'interface GigabitEthernet0/0/1',
            ' mpls ip',
            ' exit',
        ]))

if __name__ == '__main__':
    unittest.main()

