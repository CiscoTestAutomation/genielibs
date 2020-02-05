#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Igmp
from genie.libs.conf.igmp import Igmp
from genie.libs.conf.igmp.ssm import Ssm
from genie.libs.conf.igmp.igmp_group import IgmpGroup

# Vrf
from genie.libs.conf.vrf import Vrf

# Interface
from genie.libs.conf.base import IPv4Address
from genie.libs.conf.interface import IPv4Addr
from genie.libs.conf.interface import Interface

class test_igmp(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        
        # Igmp object
        self.igmp = Igmp()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # VRF configuration
        vrf1 = Vrf('VRF1')
        self.igmp.device_attr[self.dev1].require_router_alert = True
        igmp1 = self.igmp.device_attr[self.dev1].vrf_attr[vrf1]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_range = '239.1.1.0/24'
        ssm1.ssm_source_addr = '1.1.1.1'
        igmp1.add_ssm(ssm1)
        ssm2 = Ssm(device=self.dev1)
        ssm2.ssm_group_range = '239.1.1.0/24'
        ssm2.ssm_source_addr = '2.2.2.2'
        igmp1.add_ssm(ssm2)

        # Interface configuration
        intf1_obj = Interface(device=self.dev1, name='Ethernet2/4')
        intf1_obj.vrf = vrf1
        intf1 = intf1_obj.name
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .enable = True
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .robustness_variable = 7
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .group_policy = 'test2'
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .immediate_leave = True
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .max_groups = 10
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_interval = 133
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_max_response_time = 15
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .version = 3

        # join and static groups configuration
        igmp_intf1 = self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]
        join_group1 = IgmpGroup(device=self.dev1)
        join_group1.join_group = '239.1.1.1'
        join_group2 = IgmpGroup(device=self.dev1)
        join_group2.join_group = '239.3.3.3'
        join_group2.join_group_source_addr = '1.1.1.1'
        join_group3 = IgmpGroup(device=self.dev1)
        join_group3.join_group = '239.2.2.2'
        static_group1 = IgmpGroup(device=self.dev1)
        static_group1.static_group = '239.5.5.5'
        static_group2 = IgmpGroup(device=self.dev1)
        static_group2.static_group = '239.6.6.6'
        static_group2.static_group_source_addr = '2.2.2.1'
        static_group3 = IgmpGroup(device=self.dev1)
        static_group3.static_group = '239.6.6.6'
        static_group3.static_group_source_addr = '2.2.2.2'
        igmp_intf1.add_groups(join_group1)
        igmp_intf1.add_groups(join_group2)
        igmp_intf1.add_groups(join_group3)
        igmp_intf1.add_groups(static_group1)
        igmp_intf1.add_groups(static_group2)
        igmp_intf1.add_groups(static_group3)

        
        vrf2 = Vrf('default')
        igmp2 = self.igmp.device_attr[self.dev1].vrf_attr[vrf2]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_range = '239.1.2.0/24'
        ssm1.ssm_source_addr = '3.3.3.3'
        igmp2.add_ssm(ssm1)
        ssm2 = Ssm(device=self.dev1)
        ssm2.ssm_group_range = '239.1.1.0/24'
        ssm2.ssm_source_addr = '3.3.3.3'
        igmp2.add_ssm(ssm2)

        # Interface configuration
        intf2_obj = Interface(device=self.dev1, name='Ethernet2/1')
        ipv4a = IPv4Addr(device=self.dev1)
        ipv4a.ipv4 = '20.1.2.1'
        ipv4a.prefix_length = '24'
        intf2_obj.add_ipv4addr(ipv4a)

        intf2 = intf2_obj.name
        self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .enable = True

        # join and static groups configuration
        igmp_intf1 = self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]
        join_group = IgmpGroup(device=self.dev1)
        join_group.join_group = '239.3.3.3'
        join_group.join_group_source_addr = '1.1.1.1'
        static_group = IgmpGroup(device=self.dev1)
        static_group.static_group = '239.5.5.5'
        igmp_intf1.add_groups(join_group)
        igmp_intf1.add_groups(static_group)

        # Build interface config for none-default vrfs
        intf_cfgs = intf1_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface Ethernet2/4',
                ' vrf member VRF1',
                ' exit',
            ]))

        intf_cfgs = intf2_obj.build_config(apply=False)
        self.assertMultiLineEqual(
            str(intf_cfgs),
            '\n'.join([
                'interface Ethernet2/1',
                ' ip address 20.1.2.1/24',
                ' exit',
            ]))



        # Build igmp configuration
        cfgs = self.igmp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ip igmp enforce-router-alert',
                'ip igmp ssm-translate 239.1.1.0/24 3.3.3.3',
                'ip igmp ssm-translate 239.1.2.0/24 3.3.3.3',
                'interface Ethernet2/1',
                ' ip pim sparse-mode',
                ' ip igmp join-group 239.3.3.3 source 1.1.1.1',
                ' ip igmp static-oif 239.5.5.5',
                ' exit',
                'vrf context VRF1',
                ' ip igmp ssm-translate 239.1.1.0/24 1.1.1.1',
                ' ip igmp ssm-translate 239.1.1.0/24 2.2.2.2',
                ' exit',
                'interface Ethernet2/4',
                ' ip pim sparse-mode',
                ' ip igmp access-group test2',
                ' ip igmp immediate-leave',
                ' ip igmp state-limit 10',
                ' ip igmp query-interval 133',
                ' ip igmp query-max-response-time 15',
                ' ip igmp robustness-variable 7',
                ' ip igmp version 3',
                ' ip igmp join-group 239.1.1.1',
                ' ip igmp join-group 239.2.2.2',
                ' ip igmp join-group 239.3.3.3 source 1.1.1.1',
                ' ip igmp static-oif 239.5.5.5',
                ' ip igmp static-oif 239.6.6.6 source 2.2.2.1',
                ' ip igmp static-oif 239.6.6.6 source 2.2.2.2',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.igmp.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ip igmp enforce-router-alert',
                'no ip igmp ssm-translate 239.1.1.0/24 3.3.3.3',
                'no ip igmp ssm-translate 239.1.2.0/24 3.3.3.3',
                'interface Ethernet2/1',
                ' no ip pim sparse-mode',
                ' no ip igmp join-group 239.3.3.3 source 1.1.1.1',
                ' no ip igmp static-oif 239.5.5.5',
                ' exit',
                'no vrf context VRF1',
                'interface Ethernet2/4',
                ' no ip pim sparse-mode',
                ' no ip igmp access-group test2',
                ' no ip igmp immediate-leave',
                ' no ip igmp state-limit 10',
                ' no ip igmp query-interval 133',
                ' no ip igmp query-max-response-time 15',
                ' no ip igmp robustness-variable 7',
                ' no ip igmp version 3',
                ' no ip igmp join-group 239.1.1.1',
                ' no ip igmp join-group 239.2.2.2',
                ' no ip igmp join-group 239.3.3.3 source 1.1.1.1',
                ' no ip igmp static-oif 239.5.5.5',
                ' no ip igmp static-oif 239.6.6.6 source 2.2.2.1',
                ' no ip igmp static-oif 239.6.6.6 source 2.2.2.2',
                ' exit',
            ]))

        # Build unconfig with attribute
        cfgs = self.igmp.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                                        self.dev1: {
                                                            'require_router_alert': True,
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
                'no ip igmp enforce-router-alert',
                'interface Ethernet2/1',
                ' no ip pim sparse-mode',
                ' exit',
                'vrf context VRF1',
                ' no ip igmp ssm-translate 239.1.1.0/24 1.1.1.1',
                ' no ip igmp ssm-translate 239.1.1.0/24 2.2.2.2',
                ' exit',
            ]))


if __name__ == '__main__':
    unittest.main()
