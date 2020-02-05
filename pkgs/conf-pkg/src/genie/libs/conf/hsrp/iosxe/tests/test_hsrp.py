#!/usr/bin/env python

'''
IOSXE unit tests for Genie Standby conf using CLI.
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
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')
        # Interface
        self.intf1 = Interface(name='GigabitEthernet1/0/1', device=self.dev1)
        self.intf1.shutdown = False
        self.intf1.switchport = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no shutdown',
                ' no switchport',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.preempt_sync_delay = 20
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_word = 'cisco123'
        key.bfd = True
        key.mac_refresh = 11
        key.follow = 'test'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby bfd',
                ' standby delay minimum 5 reload 10',
                ' standby mac-refresh 11',
                ' standby 1 authentication cisco123',
                ' standby 1 follow test',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt delay minimum 5 reload 10 sync 20',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby bfd',
                ' no standby delay minimum 5 reload 10',
                ' no standby mac-refresh 11',
                ' no standby 1 authentication cisco123',
                ' no standby 1 follow test',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt delay minimum 5 reload 10 sync 20',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_text = 'cisco123'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication text cisco123',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt delay minimum 5 reload 10',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication text cisco123',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt delay minimum 5 reload 10',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config3(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_md5_keychain = 'abc'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication md5 key-chain abc',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt delay minimum 5',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication md5 key-chain abc',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt delay minimum 5',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config4(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.hello_interval_seconds = 1
        key.holdtime_seconds = 3
        key.track_object = 1
        key.priority_decrement = 20
        key.authentication_md5_keystring = 'xyz'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication md5 key-string xyz',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt delay minimum 5 reload 10',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication md5 key-string xyz',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt delay minimum 5 reload 10',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config5(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.group_number = 15
        key.priority = 110
        key.preempt = True
        key.bfd = True
        key.use_bia = True
        key.hello_interval_msec = 55
        key.holdtime_msec = 100
        key.track_object = 1
        key.track_shutdown = True
        key.group_name = 'gandalf'
        key.mac_address = 'dead.beef.dead'
        key.redirect = True

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby bfd',
                ' standby delay minimum 5',
                ' standby use-bia',
                ' standby redirect',
                ' standby 15 mac-address dead.beef.dead',
                ' standby 15 name gandalf',
                ' standby 15 preempt',
                ' standby 15 priority 110',
                ' standby 15 timers msec 55 msec 100',
                ' standby 15 track 1 shutdown',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby bfd',
                ' no standby delay minimum 5',
                ' no standby use-bia',
                ' no standby redirect',
                ' no standby 15 mac-address dead.beef.dead',
                ' no standby 15 name gandalf',
                ' no standby 15 preempt',
                ' no standby 15 priority 110',
                ' no standby 15 timers msec 55 msec 100',
                ' no standby 15 track 1 shutdown',
                ' exit',
            ]))

    def test_cli_config6(self):
        # Hsrp object
        self.hsrp1 = Hsrp()

        # Apply configuration
        key1 = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key1.version = 2
        key1.group_number = 10
        key1.priority = 110
        key1.preempt = True
        key1.preempt_reload_delay = 30
        
        # Hsrp object
        self.hsrp2 = Hsrp()

        # Apply configuration
        key2 = self.hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key2.group_number = 20
        key2.priority = 120
        key2.preempt = True
        key2.preempt_sync_delay = 60

        # Build config
        cfgs1 = self.hsrp1.build_config(apply=False)
        cfgs2 = self.hsrp2.build_config(apply=False)

        cfgs = str(cfgs1[self.dev1.name]) + '\n' + str(cfgs2[self.dev1.name])

        # Check config correctly unconfigured
        self.assertMultiLineEqual(cfgs,
            '\n'.join([
            'interface GigabitEthernet1/0/1\n'
            ' standby version 2\n'
            ' standby 10 preempt delay reload 30\n'
            ' standby 10 priority 110\n'
            ' exit\n'
            'interface GigabitEthernet1/0/1\n'
            ' standby 20 preempt delay sync 60\n'
            ' standby 20 priority 120\n'
            ' exit'
            ]))

class test_hsrp(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')
        # Interface
        self.intf1 = Interface(name='GigabitEthernet1/0/1', device=self.dev1)
        self.intf1.enabled = False
        self.intf1.switchport = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' shutdown',
                ' no switchport',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20
        key.authentication = 'cisco123'
        key.bfd_enabled = True
        key.mac_refresh = 11
        key.follow = 'test'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby bfd',
                ' standby delay minimum 5 reload 10',
                ' standby mac-refresh 11',
                ' standby 1 authentication cisco123',
                ' standby 1 follow test',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby bfd',
                ' no standby delay minimum 5 reload 10',
                ' no standby mac-refresh 11',
                ' no standby 1 authentication cisco123',
                ' no standby 1 follow test',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.254'
        key.secondary_ipv4_address = '192.168.1.253'
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20
        key.authentication = 'cisco123'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication cisco123',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 ip 192.168.1.253 secondary',
                ' standby 1 preempt',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication cisco123',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 ip 192.168.1.253 secondary',
                ' no standby 1 preempt',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config3(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.254'
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20
        key.authentication = 'abc'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication abc',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 preempt',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication abc',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 preempt',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config4(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.254'
        key.virtual_ip_learn = True
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20
        key.authentication = 'xyz'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby delay minimum 5 reload 10',
                ' standby 1 authentication xyz',
                ' standby 1 ip 192.168.1.254',
                ' standby 1 ip',
                ' standby 1 preempt',
                ' standby 1 priority 110',
                ' standby 1 timers 1 3',
                ' standby 1 track 1 decrement 20',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby delay minimum 5 reload 10',
                ' no standby 1 authentication xyz',
                ' no standby 1 ip 192.168.1.254',
                ' no standby 1 ip',
                ' no standby 1 preempt',
                ' no standby 1 priority 110',
                ' no standby 1 timers 1 3',
                ' no standby 1 track 1 decrement 20',
                ' exit',
            ]))

    def test_cli_config5(self):
        # Apply configuration
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.address_family = 'ipv6'
        key.global_ipv6_address = '2001:db8::1/24'
        key.link_local_ipv6_address = 'fe80::1'
        key.hsrp_linklocal = 'auto'
        key.minimum_delay = 5
        key.group_number = 15
        key.priority = 110
        key.preempt = True
        key.bfd_enabled = True
        key.use_bia = True
        key.hello_msec_flag = True
        key.hello_msec = 55
        key.hold_msec_flag = True
        key.hold_msec = 100
        key.tracked_object = 1
        key.session_name = 'gandalf'
        key.virtual_mac_address = 'dead.beef.dead'
        key.redirects_disable = False

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' standby version 2',
                ' standby bfd',
                ' standby delay minimum 5',
                ' standby use-bia',
                ' standby redirect',
                ' standby 15 ipv6 2001:db8::1/24',
                ' standby 15 ipv6 fe80::1',
                ' standby 15 ipv6 autoconfig',
                ' standby 15 mac-address dead.beef.dead',
                ' standby 15 name gandalf',
                ' standby 15 preempt',
                ' standby 15 priority 110',
                ' standby 15 timers msec 55 msec 100',
                ' standby 15 track 1',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'interface GigabitEthernet1/0/1',
                ' no standby version 2',
                ' no standby bfd',
                ' no standby delay minimum 5',
                ' no standby use-bia',
                ' no standby redirect',
                ' no standby 15 ipv6 2001:db8::1/24',
                ' no standby 15 ipv6 fe80::1',
                ' no standby 15 ipv6 autoconfig',
                ' no standby 15 mac-address dead.beef.dead',
                ' no standby 15 name gandalf',
                ' no standby 15 preempt',
                ' no standby 15 priority 110',
                ' no standby 15 timers msec 55 msec 100',
                ' no standby 15 track 1',
                ' exit',
            ]))

    def test_cli_config6(self):
        # Hsrp object
        self.hsrp1 = Hsrp()

        # Apply configuration
        key1 = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key1.version = 2
        key1.group_number = 10
        key1.priority = 110
        key1.preempt = True
        
        # Hsrp object
        self.hsrp2 = Hsrp()

        # Apply configuration
        key2 = self.hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key2.group_number = 20
        key2.priority = 120
        key2.preempt = True

        # Build config
        cfgs1 = self.hsrp1.build_config(apply=False)
        cfgs2 = self.hsrp2.build_config(apply=False)

        cfgs = str(cfgs1[self.dev1.name]) + '\n' + str(cfgs2[self.dev1.name])

        # Check config correctly unconfigured
        self.assertMultiLineEqual(cfgs,
            '\n'.join([
            'interface GigabitEthernet1/0/1\n'
            ' standby version 2\n'
            ' standby 10 preempt\n'
            ' standby 10 priority 110\n'
            ' exit\n'
            'interface GigabitEthernet1/0/1\n'
            ' standby 20 preempt\n'
            ' standby 20 priority 120\n'
            ' exit'
            ]))

if __name__ == '__main__':
    unittest.main()

