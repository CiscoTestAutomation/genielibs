#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Mld
from genie.libs.conf.mld import Mld
from genie.libs.conf.mld.ssm import Ssm
from genie.libs.conf.mld.mld_group import MldGroup

# Vrf
from genie.libs.conf.vrf import Vrf

# Interface
from genie.libs.conf.interface import IPv6Addr
from genie.libs.conf.interface import Interface

class test_mld(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        
        # Mld object
        self.mld = Mld()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # VRF configuration
        vrf1 = Vrf('VRF1')
        self.mld.device_attr[self.dev1].require_router_alert = True
        mld1 = self.mld.device_attr[self.dev1].vrf_attr[vrf1]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_range = 'ff31::1/128'
        ssm1.ssm_source_addr = '2001:db8:1:1::1'
        mld1.add_ssm(ssm1)
        ssm2 = Ssm(device=self.dev1)
        ssm2.ssm_group_range = 'ff32::1/128'
        ssm2.ssm_source_addr = '2001:db8:1:1::1'
        mld1.add_ssm(ssm2)

        # Interface configuration
        intf1_obj = Interface(device=self.dev1, name='Ethernet2/2')
        intf1_obj.vrf = vrf1
        intf1 = intf1_obj.name
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .enable = True
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .robustness_variable = 7
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .group_policy = 'test2'
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .immediate_leave = True
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .max_groups = 6400
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_interval = 366
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_max_response_time = 15
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .version = 2

        # join and static groups configuration
        mld_intf1 = self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]
        join_group1 = MldGroup(device=self.dev1)
        join_group1.join_group = 'fffe::1'
        join_group2 = MldGroup(device=self.dev1)
        join_group2.join_group = 'ff30::1'
        join_group2.join_group_source_addr = '2001:db8:0:abcd::1'
        static_group1 = MldGroup(device=self.dev1)
        static_group1.static_group = 'fffe::2'
        static_group2 = MldGroup(device=self.dev1)
        static_group2.static_group = 'ff30::2'
        static_group2.static_group_source_addr = '2001:db8:0:abcd::2'
        mld_intf1.add_groups(join_group1)
        mld_intf1.add_groups(join_group2)
        mld_intf1.add_groups(static_group1)
        mld_intf1.add_groups(static_group2)

        
        vrf2 = Vrf('default')
        mld2 = self.mld.device_attr[self.dev1].vrf_attr[vrf2]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_range = 'ff31::1/128'
        ssm1.ssm_source_addr = '2001:db8:1:1::1'
        mld2.add_ssm(ssm1)
        ssm2 = Ssm(device=self.dev1)
        ssm2.ssm_group_range = 'ff31::1/128'
        ssm2.ssm_source_addr = '2001:db8:1:1::2'
        mld2.add_ssm(ssm2)

        # Interface configuration
        intf2_obj = Interface(device=self.dev1, name='Ethernet2/1')
        ipv6a = IPv6Addr(device=self.dev1)
        ipv6a.ipv6 = '2001:db1:1:1::1'
        ipv6a.ipv6_prefix_length = '64'
        intf2_obj.add_ipv6addr(ipv6a)

        intf2 = intf2_obj.name
        self.mld.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .enable = True

        # join and static groups configuration
        mld_intf1 = self.mld.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]
        join_group = MldGroup(device=self.dev1)
        join_group.join_group = 'ff30::1'
        join_group.join_group_source_addr = '2001:db8:0:abcd::1'
        static_group = MldGroup(device=self.dev1)
        static_group.static_group = 'fffe::2'
        mld_intf1.add_groups(join_group)
        mld_intf1.add_groups(static_group)

        # Build interface config for none-default vrfs
        intf_cfgs = intf1_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface Ethernet2/2',
                ' vrf member VRF1',
                ' exit',
            ]))

        intf_cfgs = intf2_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface Ethernet2/1',
                ' ipv6 address 2001:db1:1:1::1/64',
                ' exit',
            ]))



        # Build mld configuration
        cfgs = self.mld.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::1',
                'ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::2',
                'interface Ethernet2/1',
                ' ipv6 pim sparse-mode',
                ' ipv6 mld join-group ff30::1 source 2001:db8:0:abcd::1',
                ' ipv6 mld static-oif fffe::2',
                ' exit',
                'vrf context VRF1',
                ' ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::1',
                ' ipv6 mld ssm-translate ff32::1/128 2001:db8:1:1::1',
                ' exit',
                'interface Ethernet2/2',
                ' ipv6 pim sparse-mode',
                ' ipv6 mld access-group test2',
                ' ipv6 mld immediate-leave',
                ' ipv6 mld state-limit 6400',
                ' ipv6 mld query-interval 366',
                ' ipv6 mld query-max-response-time 15',
                ' ipv6 mld robustness-variable 7',
                ' ipv6 mld version 2',
                ' ipv6 mld join-group ff30::1 source 2001:db8:0:abcd::1',
                ' ipv6 mld static-oif ff30::2 source 2001:db8:0:abcd::2',
                ' ipv6 mld join-group fffe::1',
                ' ipv6 mld static-oif fffe::2',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.mld.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::1',
                'no ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::2',
                'interface Ethernet2/1',
                ' no ipv6 pim sparse-mode',
                ' no ipv6 mld join-group ff30::1 source 2001:db8:0:abcd::1',
                ' no ipv6 mld static-oif fffe::2',
                ' exit',
                'no vrf context VRF1',
                'interface Ethernet2/2',
                ' no ipv6 pim sparse-mode',
                ' no ipv6 mld access-group test2',
                ' no ipv6 mld immediate-leave',
                ' no ipv6 mld state-limit 6400',
                ' no ipv6 mld query-interval 366',
                ' no ipv6 mld query-max-response-time 15',
                ' no ipv6 mld robustness-variable 7',
                ' no ipv6 mld version 2',
                ' no ipv6 mld join-group ff30::1 source 2001:db8:0:abcd::1',
                ' no ipv6 mld static-oif ff30::2 source 2001:db8:0:abcd::2',
                ' no ipv6 mld join-group fffe::1',
                ' no ipv6 mld static-oif fffe::2',
                ' exit',
            ]))

        # Build unconfig with attribute
        cfgs = self.mld.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                                        self.dev1: {
                                                            'vrf_attr': {
                                                                vrf1: {
                                                                    'ssm': None,},
                                                                vrf2: {
                                                                    'interface_attr': {
                                                                        'Ethernet2/1': {
                                                                            'enable': True
                                                                        }
                                                                    }
                                                                }}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface Ethernet2/1',
                ' no ipv6 pim sparse-mode',
                ' exit',
                'vrf context VRF1',
                ' no ipv6 mld ssm-translate ff31::1/128 2001:db8:1:1::1',
                ' no ipv6 mld ssm-translate ff32::1/128 2001:db8:1:1::1',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()
