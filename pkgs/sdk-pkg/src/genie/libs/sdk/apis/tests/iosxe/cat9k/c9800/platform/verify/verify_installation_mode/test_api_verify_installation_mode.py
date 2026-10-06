import unittest
from unittest.mock import Mock

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_installation_mode,
)


SHOW_VERSION = '''
Cisco IOS XE Software, Version BLD_V179_THROTTLE_LATEST_20220506_192009
Cisco IOS Software [Cupertino], C9800-CL Software (C9800-CL-K9_IOSXE), Experimental Version 17.9.20220506:200143
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Fri 06-May-22 13:01 by mcpre

ROM: IOS-XE ROMMON

vidya-ewlc-5 uptime is 3 weeks, 6 days, 13 hours, 26 minutes
Uptime for this control processor is 3 weeks, 6 days, 13 hours, 30 minutes
System returned to ROM by reload
System restarted at 13:54:07 UTC Thu May 12 2022
System image file is "bootflash:packages.conf"
Last reload reason: Install

AIR License Level: AIR DNA Advantage
Next reload AIR license Level: AIR DNA Advantage

Smart Licensing Status: Smart Licensing Using Policy

cisco C9800-CL (VXE) processor (revision VXE) with 12266721K/3075K bytes of memory.
Processor board ID 9SV9FR9MWP9
Router operating mode: Autonomous
5 Virtual Ethernet interfaces
3 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
16332132K bytes of physical memory.
6201343K bytes of virtual hard disk at bootflash:.
Installation mode is INSTALL

Configuration register is 0x102
'''


class TestVerifyInstallationMode(unittest.TestCase):

    def setUp(self):
        self.device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        self.device.is_connected = Mock(return_value=True)
        self.device.cli = self.device
        self.device.execute = Mock(
            side_effect=lambda command: {'show version': SHOW_VERSION}[command])

    def test_verify_installation_mode(self):
        result = verify_installation_mode(self.device, 'INSTALL')

        self.assertTrue(result)
        self.device.execute.assert_called_once_with('show version')

    def test_verify_installation_mode_mismatch(self):
        result = verify_installation_mode(self.device, 'BUNDLE')

        self.assertFalse(result)
