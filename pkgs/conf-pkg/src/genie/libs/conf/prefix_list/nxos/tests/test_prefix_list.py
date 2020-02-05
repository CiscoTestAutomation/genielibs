#!/usr/bin/env python

'''
NXOS unit tests for Genie prefix-list conf using CLI.
'''

# Python
import re
import unittest
from unittest.mock import Mock

# Genie
from genie.conf import Genie
from genie.tests.conf import TestCase
from genie.conf.base import Testbed, Device
from genie.libs.conf.prefix_list.prefix_list import PrefixList


class test_prefix_list(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')

    def test_cli_config_v4(self):        
        # prefix-list conf
        prefix_conf = PrefixList(prefix_set_name='test')
        self.dev1.add_feature(prefix_conf)
        # Apply configuration
        prefix_conf.device_attr[self.dev1].prefix_attr['35.0.0.0/8'].\
            maxlength_range_attr['8..8'].protocol = 'ipv4'
        prefix_conf.device_attr[self.dev1].prefix_attr['35.0.0.0/8'].\
            maxlength_range_attr['8..16'].protocol = 'ipv4'
        prefix_conf.device_attr[self.dev1].prefix_attr['37.0.0.0/8'].\
            maxlength_range_attr['16..24'].protocol = 'ipv4'
        prefix_conf.device_attr[self.dev1].prefix_attr['38.0.0.0/8'].\
            maxlength_range_attr['16..32'].protocol = 'ipv4'
        prefix_conf.device_attr[self.dev1].prefix_attr['2001:DB8:4::/64']\
            .maxlength_range_attr['65..98'].protocol = 'ipv6'

        # Build config
        cfgs = prefix_conf.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ipv6 prefix-list test permit 2001:DB8:4::/64 ge 65 le 98',
                'ip prefix-list test permit 35.0.0.0/8 le 16',
                'ip prefix-list test permit 35.0.0.0/8',
                'ip prefix-list test permit 37.0.0.0/8 ge 16 le 24',
                'ip prefix-list test permit 38.0.0.0/8 ge 16',
            ]))

        # Build unconfig
        cfgs = prefix_conf.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ipv6 prefix-list test permit 2001:DB8:4::/64 ge 65 le 98',
                'no ip prefix-list test permit 35.0.0.0/8 le 16',
                'no ip prefix-list test permit 35.0.0.0/8',
                'no ip prefix-list test permit 37.0.0.0/8 ge 16 le 24',
                'no ip prefix-list test permit 38.0.0.0/8 ge 16',
            ]))

    def test_cli_config_v6(self):
        # prefix-list conf
        prefix_conf_v6 = PrefixList(prefix_set_name='test6')
        prefix_conf_v6.device_attr[self.dev1].prefix_attr['2001:DB8:1::/64']\
            .maxlength_range_attr['64..64'].protocol = 'ipv6'
        prefix_conf_v6.device_attr[self.dev1].prefix_attr['2001:DB8:2::/64']\
            .maxlength_range_attr['65..128'].protocol = 'ipv6'
        prefix_conf_v6.device_attr[self.dev1].prefix_attr['2001:DB8:3::/64']\
            .maxlength_range_attr['64..128'].protocol = 'ipv6'
        prefix_conf_v6.device_attr[self.dev1].prefix_attr['2001:DB8:4::/64']\
            .maxlength_range_attr['65..98'].protocol = 'ipv6'

        # Build config
        cfgs = prefix_conf_v6.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'ipv6 prefix-list test6 permit 2001:DB8:1::/64',
                'ipv6 prefix-list test6 permit 2001:DB8:2::/64 ge 65',
                'ipv6 prefix-list test6 permit 2001:DB8:3::/64 le 128',
                'ipv6 prefix-list test6 permit 2001:DB8:4::/64 ge 65 le 98',
            ]))

        # Build unconfig
        cfgs = prefix_conf_v6.build_unconfig(apply=False)
        
        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ipv6 prefix-list test6 permit 2001:DB8:1::/64',
                'no ipv6 prefix-list test6 permit 2001:DB8:2::/64 ge 65',
                'no ipv6 prefix-list test6 permit 2001:DB8:3::/64 le 128',
                'no ipv6 prefix-list test6 permit 2001:DB8:4::/64 ge 65 le 98',
            ]))


if __name__ == '__main__':
    unittest.main()

