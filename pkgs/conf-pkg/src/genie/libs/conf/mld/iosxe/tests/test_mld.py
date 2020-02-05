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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')
        
        # Mld object
        self.mld = Mld()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # VRF configuration
        vrf1 = Vrf('VRF1')
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].global_max_groups = 63999
        mld1 = self.mld.device_attr[self.dev1].vrf_attr[vrf1]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_policy = 'test'
        ssm1.ssm_source_addr = '2001:DB8:1:1::1'
        mld1.add_ssm(ssm1)

        # Interface configuration
        intf1_obj = Interface(device=self.dev1, name='GigabitEthernet2')
        intf1_obj.vrf = vrf1
        intf1 = intf1_obj.name
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .enable = True
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .group_policy = 'test2'
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .max_groups = 6400
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_interval = 366
        self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_max_response_time = 16

        # join and static groups configuration
        mld_intf1 = self.mld.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]
        join_group1 = MldGroup(device=self.dev1)
        join_group1.join_group = 'FF25:2::1'
        join_group2 = MldGroup(device=self.dev1)
        join_group2.join_group = 'FF15:1::1'
        join_group2.join_group_source_addr = '2001:DB8:2:2::2'
        static_group1 = MldGroup(device=self.dev1)
        static_group1.static_group = 'FF45:1::1'
        static_group2 = MldGroup(device=self.dev1)
        static_group2.static_group = 'FF35:1::1'
        static_group2.static_group_source_addr = '2001:DB8:3:3::3'
        mld_intf1.add_groups(join_group1)
        mld_intf1.add_groups(join_group2)
        mld_intf1.add_groups(static_group1)
        mld_intf1.add_groups(static_group2)

        
        vrf2 = Vrf('default')
        self.mld.device_attr[self.dev1].vrf_attr[vrf2].global_max_groups = 63999
        mld2 = self.mld.device_attr[self.dev1].vrf_attr[vrf2]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_policy = 'test'
        ssm1.ssm_source_addr = '2001:DB8:1:1::1'
        mld2.add_ssm(ssm1)

        # Interface configuration
        intf2_obj = Interface(device=self.dev1, name='GigabitEthernet1')
        ipv6a = IPv6Addr(device=self.dev1)
        ipv6a.ipv6 = '2001:DB8:1:1::1'
        ipv6a.ipv6_prefix_length = '64'
        intf2_obj.add_ipv6addr(ipv6a)

        intf2 = intf2_obj.name
        self.mld.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .enable = True

        # join and static groups configuration
        mld_intf1 = self.mld.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]
        join_group = MldGroup(device=self.dev1)
        join_group.join_group = 'FF15:1::1'
        join_group.join_group_source_addr = '2001:DB8:2:2::2'
        static_group = MldGroup(device=self.dev1)
        static_group.static_group = 'FF45:1::1'
        mld_intf1.add_groups(join_group)
        mld_intf1.add_groups(static_group)

        # Build interface config for none-default vrfs
        intf_cfgs = intf1_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface GigabitEthernet2',
                ' vrf forwarding VRF1',
                ' exit',
            ]))

        intf_cfgs = intf2_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface GigabitEthernet1',
                ' ipv6 address 2001:db8:1:1::1/64',
                ' exit',
            ]))



        # Build mld configuration
        cfgs = self.mld.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ipv6 mld state-limit 63999',
                'ipv6 mld ssm-map enable',
                'ipv6 mld ssm-map static test 2001:DB8:1:1::1',
                'interface GigabitEthernet1',
                ' ipv6 mld router',
                ' ipv6 mld join-group FF15:1::1 2001:DB8:2:2::2',
                ' ipv6 mld static-group FF45:1::1',
                ' exit',
                'ipv6 mld vrf VRF1 state-limit 63999',
                'ipv6 mld vrf VRF1 ssm-map enable',
                'ipv6 mld vrf VRF1 ssm-map static test 2001:DB8:1:1::1',
                'interface GigabitEthernet2',
                ' ipv6 mld router',
                ' ipv6 mld access-group test2',
                ' ipv6 mld limit 6400',
                ' ipv6 mld query-interval 366',
                ' ipv6 mld query-max-response-time 16',
                ' ipv6 mld join-group FF15:1::1 2001:DB8:2:2::2',
                ' ipv6 mld join-group FF25:2::1',
                ' ipv6 mld static-group FF35:1::1 2001:DB8:3:3::3',
                ' ipv6 mld static-group FF45:1::1',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.mld.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ipv6 mld state-limit 63999',
                'no ipv6 mld ssm-map enable',
                'no ipv6 mld ssm-map static test 2001:DB8:1:1::1',
                'interface GigabitEthernet1',
                ' no ipv6 mld router',
                ' no ipv6 mld join-group FF15:1::1 2001:DB8:2:2::2',
                ' no ipv6 mld static-group FF45:1::1',
                ' exit',
                'no ipv6 mld vrf VRF1 state-limit 63999',
                'no ipv6 mld vrf VRF1 ssm-map enable',
                'no ipv6 mld vrf VRF1 ssm-map static test 2001:DB8:1:1::1',
                'interface GigabitEthernet2',
                ' no ipv6 mld router',
                ' no ipv6 mld access-group test2',
                ' no ipv6 mld limit 6400',
                ' no ipv6 mld query-interval 366',
                ' no ipv6 mld query-max-response-time 16',
                ' no ipv6 mld join-group FF15:1::1 2001:DB8:2:2::2',
                ' no ipv6 mld join-group FF25:2::1',
                ' no ipv6 mld static-group FF35:1::1 2001:DB8:3:3::3',
                ' no ipv6 mld static-group FF45:1::1',
                ' exit',
            ]))

        # Build unconfig with attribute
        cfgs = self.mld.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                                        self.dev1: {
                                                            'vrf_attr': {
                                                                vrf1: {
                                                                    'global_max_groups': None,
                                                                    'ssm': {ssm1: None}},
                                                                vrf2: {
                                                                    'interface_attr': {
                                                                        'GigabitEthernet1': {
                                                                            'enable': True
                                                                        }
                                                                    }
                                                                }}}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1',
                ' no ipv6 mld router',
                ' exit',
                'no ipv6 mld vrf VRF1 state-limit 63999',
                'no ipv6 mld vrf VRF1 ssm-map enable',
                'no ipv6 mld vrf VRF1 ssm-map static test 2001:DB8:1:1::1',
            ]))


if __name__ == '__main__':
    unittest.main()
