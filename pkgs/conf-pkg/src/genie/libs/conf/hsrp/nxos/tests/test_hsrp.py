#!/usr/bin/env python

'''
NXOS unit tests for Genie Hsrp conf.
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
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        # Interface
        self.intf1 = Interface(name='Ethernet2/1', device=self.dev1)
        self.intf1.enabled = True
        self.intf1.switchport_enable = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)
        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet2/1',
                ' no shutdown',
                ' no switchport',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.bfd = True
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.use_bia = True
        key.group_number = 1
        key.authentication_word = 'cisco123'
        key.ip_address = '192.168.1.1/24'
        key.mac_address = 'dead.beef.dead'
        key.group_name = 'gandalf'
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.preempt_sync_delay = 20
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
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp bfd',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp use-bia',
                ' hsrp 1',
                '  authentication cisco123',
                '  ip 192.168.1.1/24',
                '  mac-address dead.beef.dead',
                '  name gandalf',
                '  preempt delay minimum 5 reload 10 sync 20',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp bfd',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp use-bia',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
        key.preempt_minimum_delay = 5
        key.preempt_reload_delay = 10
        key.hello_interval_msec = 300
        key.holdtime_msec = 500
        key.track_object = 1
        key.authentication_text = 'cisco123'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp 1',
                '  authentication text cisco123',
                '  ip 192.168.1.1/24',
                '  preempt delay minimum 5 reload 10',
                '  priority 110',
                '  timers msec 300 msec 500',
                '  track 1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config3(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.1/24'
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
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp 1',
                '  authentication md5 key-chain abc',
                '  ip 192.168.1.1/24',
                '  preempt delay minimum 5',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config4(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.ip_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
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
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp 1',
                '  authentication md5 key-string xyz',
                '  ip 192.168.1.1/24',
                '  preempt delay reload 10',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config5(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.group_number = 9
        key.ip_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
        key.preempt_sync_delay = 10

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5',
                ' hsrp 9',
                '  ip 192.168.1.1/24',
                '  preempt delay sync 10',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5',
                ' no hsrp 9',
                ' exit',
            ]))

    def test_cli_config6(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.group_number = 9
        key.ip_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 9',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 9',
                ' exit',
            ]))

    def test_cli_config_args(self):
        # create Hsrp conf by taking args
        hsrp1 = Hsrp(group_number=0, address_family = 'ipv6')
        # Apply configuration
        hsrp1.device_attr[self.dev1].enabled = True
        key = hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.ip_address = '192:168::1:1:1/128'
        key.priority = 110
        key.preempt = True
        # create Hsrp conf by taking args
        hsrp2 = Hsrp(group_number=0)
        # Apply configuration
        hsrp2.device_attr[self.dev1].enabled = True
        key = hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.ip_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True

        # Build config
        cfgs_1 = hsrp1.build_config(apply=False)# Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs_1[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 0 ipv6',
                '  ipv6 192:168::1:1:1/128',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs_1 = hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs_1[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 0 ipv6',
                ' exit',
            ]))

        cfgs_2 = hsrp2.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs_2[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 0',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs_2 = hsrp2.build_unconfig(apply=False)
        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs_2[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 0',
                ' exit',
            ]))

class test_hsrp(TestCase):

    def setUp(self):
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        # Interface
        self.intf1 = Interface(name='Ethernet2/1', device=self.dev1)
        self.intf1.enabled = True
        self.intf1.switchport_enable = False
        # Hsrp object
        self.hsrp1 = Hsrp()
        # Build config
        cfgs = self.intf1.build_config(apply=False)
        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs),
            '\n'.join([
                'interface Ethernet2/1',
                ' no shutdown',
                ' no switchport',
                ' exit',
            ]))

    def test_cli_config1(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.bfd_enabled = True
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.use_bia = True
        key.group_number = 1
        key.authentication = 'cisco123'
        key.primary_ipv4_address = '192.168.1.1/24'
        key.secondary_ipv4_address = '192.168.1.2/24'
        key.virtual_mac_address = 'dead.beef.dead'
        key.session_name = 'gandalf'
        key.preempt = True
        key.priority = 110
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement = 20

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp bfd',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp use-bia',
                ' hsrp 1',
                '  authentication cisco123',
                '  ip 192.168.1.1/24',
                '  ip 192.168.1.2/24 secondary',
                '  mac-address dead.beef.dead',
                '  name gandalf',
                '  preempt',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp bfd',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp use-bia',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config2(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
        key.hello_msec_flag = True
        key.hello_msec = 300
        key.hold_msec_flag = True
        key.hold_msec = 500
        key.tracked_object = 1
        key.authentication = 'cisco123'
        key.follow = 'group10'
        key.mac_refresh = 199

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp mac-refresh 199',
                ' hsrp 1',
                '  authentication cisco123',
                '  ip 192.168.1.1/24',
                '  follow group10',
                '  preempt',
                '  priority 110',
                '  timers msec 300 msec 500',
                '  track 1',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp mac-refresh 199',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config3(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement= 20
        key.authentication = 'abc'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp 1',
                '  authentication abc',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config4(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.reload_delay = 10
        key.group_number = 1
        key.primary_ipv4_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True
        key.hello_sec = 1
        key.hold_sec = 3
        key.tracked_object = 1
        key.tracked_object_priority_decrement= 20
        key.authentication = 'xyz'

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5 reload 10',
                ' hsrp 1',
                '  authentication xyz',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  timers 1 3',
                '  track 1 decrement 20',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5 reload 10',
                ' no hsrp 1',
                ' exit',
            ]))

    def test_cli_config5(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 2
        key.minimum_delay = 5
        key.group_number = 9
        key.primary_ipv4_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp version 2',
                ' hsrp delay minimum 5',
                ' hsrp 9',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp version 2',
                ' no hsrp delay minimum 5',
                ' no hsrp 9',
                ' exit',
            ]))

    def test_cli_config6(self):
        # Apply configuration
        self.hsrp1.device_attr[self.dev1].enabled = True
        key = self.hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.group_number = 9
        key.virtual_ip_learn = True
        key.priority = 110
        key.preempt = True

        # Build config
        cfgs = self.hsrp1.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 9',
                '  ip',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs = self.hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 9',
                ' exit',
            ]))

    def test_cli_config_args(self):
        # create Hsrp conf by taking args
        hsrp1 = Hsrp(group_number=0, address_family = 'ipv6')
        # Apply configuration
        hsrp1.device_attr[self.dev1].enabled = True
        key = hsrp1.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.global_ipv6_address = '192:168::1:1:1/128'
        key.link_local_ipv6_address = 'fe80::1'
        key.hsrp_linklocal = 'auto'
        key.priority = 110
        key.preempt = True
        # create Hsrp conf by taking args
        hsrp2 = Hsrp(group_number=0)
        # Apply configuration
        hsrp2.device_attr[self.dev1].enabled = True
        key = hsrp2.device_attr[self.dev1].interface_attr[self.intf1]
        key.version = 1
        key.minimum_delay = 5
        key.primary_ipv4_address = '192.168.1.1/24'
        key.priority = 110
        key.preempt = True

        # Build config
        cfgs_1 = hsrp1.build_config(apply=False)# Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs_1[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 0 ipv6',
                '  ip 192:168::1:1:1/128',
                '  ip fe80::1',
                '  ip autoconfig',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs_1 = hsrp1.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs_1[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 0 ipv6',
                ' exit',
            ]))

        cfgs_2 = hsrp2.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs_2[self.dev1.name]),
            '\n'.join([
                'feature hsrp',
                'interface Ethernet2/1',
                ' hsrp delay minimum 5',
                ' hsrp 0',
                '  ip 192.168.1.1/24',
                '  preempt',
                '  priority 110',
                '  exit',
                ' exit',
            ]))

        # Build unconfig
        cfgs_2 = hsrp2.build_unconfig(apply=False)
        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs_2[self.dev1.name]),
            '\n'.join([
                'no feature hsrp',
                'interface Ethernet2/1',
                ' no hsrp delay minimum 5',
                ' no hsrp 0',
                ' exit',
            ]))

if __name__ == '__main__':
    unittest.main()

