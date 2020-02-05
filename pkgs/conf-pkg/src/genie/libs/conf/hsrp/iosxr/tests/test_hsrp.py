#!/usr/bin/env python

'''
IOSXR unit tests for Genie Hsrp conf.
'''

# Python
import re
import unittest
from unittest.mock import Mock

# Genie
from genie.conf import Genie
from genie.tests.conf import TestCase
from genie.conf.base import Testbed, Device
from genie.libs.conf.hsrp.hsrp import Hsrp
from genie.libs.conf.interface import Interface


class test_hsrp_old(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        # Interface
        self.intf1 = Interface(name='GigabitEthernet0/0/0/1', device=self.dev1)
        self.intf1.shutdown = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/1',
                ' no shutdown',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.bfd_min_interval = 30
        key.bfd_multiplier = 50
        key.minimum_delay = 5
        key.reload_delay = 10
        key.mac_refresh = 20
        key.use_bia = True
        key.redirect = True
        key.address_family = 'ipv4'
        key.version = 2
        key.group_number = 30
        key.ip_address = '192.168.1.254'
        key.authentication_word = 'cisco123'
        key.bfd_fast_detect = True
        key.mac_address = 'dead.beef.dead'
        key.group_name = 'gandalf'
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.priority = 110
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' hsrp bfd minimum-interval 30',
                ' hsrp bfd multiplier 50',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp use-bia',
                ' hsrp redirect disable',
                ' hsrp mac-refresh 20',
                ' address-family ipv4',
                '  hsrp version 2',
                '  hsrp 30',
                '   address 192.168.1.254',
                '   authentication cisco123',
                '   bfd fast-detect',
                '   mac-address dead.beef.dead',
                '   name gandalf',
                '   preempt delay 5',
                '   priority 110',
                '   timers 1 3',
                '   track object 1 20',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no hsrp bfd minimum-interval 30',
                ' no hsrp bfd multiplier 50',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp use-bia',
                ' no hsrp redirect disable',
                ' no hsrp mac-refresh 20',
                ' no address-family ipv4',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.address_family = 'ipv6'
        key.group_number = 5
        key.priority = 110
        key.preempt = True
        key.hello_interval_msec = 300
        key.holdtime_msec = 500

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv6',
                '  hsrp 5',
                '   preempt',
                '   priority 110',
                '   timers msec 300 msec 500',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv6',
                ' exit',
            ]))

    def test_cli_config_args(self):
        # create Hsrp conf by taking args
        hsrp1 = Hsrp(group_number=5, address_family = 'ipv6')
        # Apply configuration
        key = hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.priority = 110
        key.preempt = True
        key.hello_interval_msec = 300
        key.holdtime_msec = 500

        # Build config
        cfgs = hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv6',
                '  hsrp 5',
                '   preempt',
                '   priority 110',
                '   timers msec 300 msec 500',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv6',
                ' exit',
            ]))


        # create Ipv4 Hsrp conf by taking args
        hsrp2 = Hsrp(group_number=5)
        # Apply configuration
        key = hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key.priority = 110
        key.preempt = True
        key.hello_interval_msec = 300
        key.holdtime_msec = 500

        # Build config
        cfgs = hsrp2.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv4',
                '  hsrp 5',
                '   preempt',
                '   priority 110',
                '   timers msec 300 msec 500',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = hsrp2.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv4',
                ' exit',
            ]))

class test_hsrp(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxr')
        # Interface
        self.intf1 = Interface(name='GigabitEthernet0/0/0/1', device=self.dev1)
        self.intf1.shutdown = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet0/0/0/1',
                ' no shutdown',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.bfd_interval = 30
        key.bfd_detection_multiplier = 50
        key.bfd_address = '192.168.1.2'
        key.bfd_interface_name = 'GigabitEthernet0/0/0/1'
        key.minimum_delay = 5
        key.reload_delay = 10
        key.mac_refresh = 20
        key.use_bia = True
        key.redirects_disable = True
        key.address_family = 'ipv4'
        key.version = 2
        key.group_number = 30
        key.primary_ipv4_address = '192.168.1.254'
        key.secondary_ipv4_address = '192.168.1.253'
        key.authentication = 'cisco123'
        key.bfd_enabled = True
        key.virtual_mac_address = 'dead.beef.dead'
        key.session_name = 'gandalf'
        key.preempt = True
        key.priority = 110
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20
        key.state_change_disable = True

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'message state disable',
                'interface GigabitEthernet0/0/0/1',
                ' hsrp bfd minimum-interval 30',
                ' hsrp bfd multiplier 50',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp use-bia',
                ' hsrp redirect disable',
                ' hsrp mac-refresh 20',
                ' address-family ipv4',
                '  hsrp version 2',
                '  hsrp bfd fast-detect peer 192.168.1.2 GigabitEthernet0/0/0/1',
                '  hsrp 30',
                '   address 192.168.1.254',
                '   address 192.168.1.253 secondary',
                '   authentication cisco123',
                '   bfd fast-detect',
                '   mac-address dead.beef.dead',
                '   name gandalf',
                '   preempt',
                '   priority 110',
                '   timers 1 3',
                '   track object 1 20',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'no message state disable',
                'interface GigabitEthernet0/0/0/1',
                ' no hsrp bfd minimum-interval 30',
                ' no hsrp bfd multiplier 50',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp use-bia',
                ' no hsrp redirect disable',
                ' no hsrp mac-refresh 20',
                ' no address-family ipv4',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.address_family = 'ipv6'
        key.global_ipv6_address = '2001:db8:1:1::254/64'
        key.link_local_ipv6_address = 'fe80::205:73ff:fea0:19'
        key.group_number = 5
        key.priority = 110
        key.preempt = True
        key.hello_msec_flag = True
        key.hello_msec = 300
        key.hold_msec_flag = True
        key.hold_msec = 500
        key.tracked_interface = 'GigabitEthernet0/0/0/0'
        key.tracked_intf_priority_decrement = 20

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv6',
                '  hsrp 5',
                '   address global 2001:db8:1:1::254/64',
                '   address linklocal fe80::205:73ff:fea0:19',
                '   preempt',
                '   priority 110',
                '   timers msec 300 msec 500',
                '   track GigabitEthernet0/0/0/0 20',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv6',
                ' exit',
            ]))

    def test_cli_config_args(self):
        # create Hsrp conf by taking args
        hsrp1 = Hsrp(group_number=5, address_family = 'ipv6')
        # Apply configuration
        key = hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.hsrp_linklocal = 'auto'
        key.priority = 110
        key.preempt = True
        key.virtual_ip_learn = True
        key.hello_msec_flag = True
        key.hello_msec = 300
        key.hold_msec_flag = True
        key.hold_msec = 500

        # Build config
        cfgs = hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv6',
                '  hsrp 5',
                '   address learn',
                '   address linklocal autoconfig',
                '   preempt',
                '   priority 110',
                '   timers msec 300 msec 500',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv6',
                ' exit',
            ]))


        # create Ipv4 Hsrp conf by taking args
        hsrp2 = Hsrp(group_number=5)
        # Apply configuration
        key = hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key.priority = 110
        key.preempt = True
        key.hello_msec_flag = True
        key.hello_msec = 400
        key.hold_msec_flag = True
        key.hold_msec = 500
        key.follow = 'group10'

        # Build config
        cfgs = hsrp2.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' address-family ipv4',
                '  hsrp 5',
                '   slave follow group10',
                '   preempt',
                '   priority 110',
                '   timers msec 400 msec 500',
                '   exit',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = hsrp2.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no router hsrp',
                'interface GigabitEthernet0/0/0/1',
                ' no address-family ipv4',
                ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

