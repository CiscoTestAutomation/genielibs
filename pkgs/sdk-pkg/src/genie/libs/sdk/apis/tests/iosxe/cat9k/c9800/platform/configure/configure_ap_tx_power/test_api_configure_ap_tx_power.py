import unittest
from unittest.mock import Mock, call

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import (
    configure_ap_tx_power,
)
from unicon.core.errors import SubCommandFailure


SHOW_AP_SUMMARY = '''Number of APs: 4

AP Name                Slots AP Model           Ethernet MAC   Radio MAC      Location          Country IP Address State
------------------------------------------------------------------------------------------------------------------------
AP002C.C862.E708       2     AIR-AP1815I-A-K9   002c.c862.e708 002c.c88a.fd20 default location  US      9.4.57.125 Registered
AP188B.4500.44C8       2     AIR-AP1832I-D-K9   188b.4500.44c8 188b.4501.7c60 default location  IN      9.4.57.120 Registered
AP188B.4500.5EE8       2     AIR-AP1852I-D-K9   188b.4500.5ee8 188b.4501.e4e0 default location  IN      9.4.57.121 Registered
APCC16.7EDB.4168       2     AIR-AP2802I-D-K9   cc16.7edb.4168 a0e0.af91.9e60 default location  IN      9.4.57.119 Registered
'''


class TestConfigureApTxPower(unittest.TestCase):

    def setUp(self):
        self.device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        self.device.is_connected = Mock(return_value=True)
        self.device.cli = self.device
        self.device.execute = Mock(
            side_effect=lambda command: {'show ap summary': SHOW_AP_SUMMARY}[
                command])
        self.device.configure = Mock()
        self.device.api.execute_ap_tx_power_commands = Mock()

    def test_configure_ap_tx_power(self):
        configure_ap_tx_power(
            self.device,
            ['AP002C.C862.E708', 'AP188B.4500.44C8'],
            tx_power='2',
        )

        self.device.execute.assert_has_calls([
            call('show ap summary'),
            call('show ap summary'),
        ])
        self.device.api.execute_ap_tx_power_commands.assert_has_calls([
            call('AP002C.C862.E708', 'AIR-AP1815I-A-K9', '2'),
            call('AP188B.4500.44C8', 'AIR-AP1832I-D-K9', '2'),
        ])
        self.device.configure.assert_called_once_with([
            'ap dot11 5ghz rrm txpower 2',
            'ap dot11 24ghz rrm txpower 2',
        ])

    def test_configure_ap_tx_power_failure(self):
        self.device.api.execute_ap_tx_power_commands.side_effect = (
            SubCommandFailure('configuration failed'))

        with self.assertRaisesRegex(
                SubCommandFailure, 'Failed to configure AP transmit power'):
            configure_ap_tx_power(
                self.device, ['AP002C.C862.E708'], tx_power='2')
