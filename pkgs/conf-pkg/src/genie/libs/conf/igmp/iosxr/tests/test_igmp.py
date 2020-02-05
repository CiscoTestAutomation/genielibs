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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        
        # Igmp object
        self.igmp = Igmp()

    def test_mcast_config(self):

        # For failures
        self.maxDiff = None

        # VRF configuration
        vrf1 = Vrf('default')
        self.igmp.device_attr[self.dev1].require_router_alert = True
        igmp1 = self.igmp.device_attr[self.dev1].vrf_attr[vrf1]
        ssm1 = Ssm(device=self.dev1)
        ssm1.ssm_group_policy = 'test'
        ssm1.ssm_source_addr = '1.1.1.1'
        igmp1.add_ssm(ssm1)
        ssm2 = Ssm(device=self.dev1)
        ssm2.ssm_group_policy = 'test'
        ssm2.ssm_source_addr = '2.2.2.2'
        igmp1.add_ssm(ssm2)

        # Interface configuration
        intf1 = 'GigabitEthernet0/0/0/0'
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .enable = True
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .robustness_variable = 7
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .group_policy = 'test2'
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .max_groups = 10
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_interval = 133
        self.igmp.device_attr[self.dev1].vrf_attr[vrf1].interface_attr[intf1]\
            .query_max_response_time = 12
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

        
        # vrf2 = Vrf('VRF1')
        vrf2 = 'VRF1'
        igmp2 = self.igmp.device_attr[self.dev1].vrf_attr[vrf2]
        ssm3 = Ssm(device=self.dev1)
        ssm3.ssm_group_policy = 'test1'
        ssm3.ssm_source_addr = '3.3.3.3'
        igmp2.add_ssm(ssm3)
        ssm4 = Ssm(device=self.dev1)
        ssm4.ssm_group_policy = 'test1'
        ssm4.ssm_source_addr = '3.3.3.3'
        igmp2.add_ssm(ssm4)


        intf2_obj = Interface(device=self.dev1, name='GigabitEthernet0/0/0/3')
        intf2 = intf2_obj.name
        self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .enable = True
        self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .robustness_variable = 5
        self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]\
            .group_policy = 'test_policy'

        # join and static groups configuration
        igmp_intf1 = self.igmp.device_attr[self.dev1].vrf_attr[vrf2].interface_attr[intf2]
        join_group = IgmpGroup(device=self.dev1)
        join_group.join_group = '239.3.3.3'
        join_group.join_group_source_addr = '1.1.1.1'
        static_group = IgmpGroup(device=self.dev1)
        static_group.static_group = '239.5.5.5'
        igmp_intf1.add_groups(join_group)
        igmp_intf1.add_groups(static_group)

        # Build igmp configuration
        cfgs = self.igmp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router igmp',
                ' ssm map static 1.1.1.1 test',
                ' ssm map static 2.2.2.2 test',
                ' robustness-count 7',
                ' interface GigabitEthernet0/0/0/0',
                '  router enable',
                '  access-group test2',
                '  maximum groups-per-interface 10',
                '  query-interval 133',
                '  query-max-response-time 12',
                '  version 3',
                '  join-group 239.1.1.1',
                '  join-group 239.2.2.2',
                '  join-group 239.3.3.3 1.1.1.1',
                '  static-group 239.5.5.5',
                '  static-group 239.6.6.6 2.2.2.1',
                '  static-group 239.6.6.6 2.2.2.2',
                '  exit',
                ' vrf VRF1',
                '  ssm map static 3.3.3.3 test1',
                '  robustness-count 5',
                '  interface GigabitEthernet0/0/0/3',
                '   router enable',
                '   access-group test_policy',
                '   join-group 239.3.3.3 1.1.1.1',
                '   static-group 239.5.5.5',
                '   exit',
                '  exit',
                ' exit'
            ]))

        # Build unconfig
        cfgs = self.igmp.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router igmp',
            ]))

        # Build unconfig with attribute
        cfgs = self.igmp.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                                        self.dev1: {
                                                            'vrf_attr': {
                                                                vrf1: {
                                                                    'ssm': {ssm1: None}},
                                                                vrf2: {
                                                                    'interface_attr': {
                                                                        'GigabitEthernet0/0/0/3': {
                                                                            'enable': True
                                                                        }
                                                                    }
                                                                }}}}})
        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router igmp',
                ' no ssm map static 1.1.1.1 test',
                ' vrf VRF1',
                '  interface GigabitEthernet0/0/0/3',
                '   no router enable',
                '   exit',
                '  exit',
                ' exit'
            ]))


if __name__ == '__main__':
    unittest.main()
